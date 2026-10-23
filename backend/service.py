"""Persistent local core, independent of hosting/payment/age-assurance providers.

This is a development implementation, not a production service. Encryption is
server-side at rest, not end-to-end. No external provider approvals are implied.
"""
from __future__ import annotations
import calendar
import json
from .avatars import validate as validate_avatar, DEFAULT as DEFAULT_AVATAR
from contextlib import contextmanager
import hashlib
import hmac
import math
import re
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from cryptography.fernet import Fernet

DAY = 86400
# 'launch' retained only to reconcile historical development fixtures.
OFFER_PRICES = {'launch': 1000, 'website': 2000, 'standard': 5000}
VOUCHERS = {'KEELE_SU_10': {'amount_minor':1000, 'expires_at':1796083200}}
# 1 December 2026 00:00 UTC = end of 30 November in Europe/London.

class Problem(Exception):
    def __init__(self, status, message): self.status, self.message = status, message

def advance_month(ts):
    dt = datetime.fromtimestamp(ts, timezone.utc)
    year, month = (dt.year + 1, 1) if dt.month == 12 else (dt.year, dt.month + 1)
    return int(dt.replace(year=year, month=month, day=min(dt.day, calendar.monthrange(year, month)[1])).timestamp())

def text(value, name, minimum=1, maximum=300):
    if not isinstance(value, str): raise Problem(400, f'{name} must be text')
    value = value.strip()
    if not minimum <= len(value) <= maximum: raise Problem(400, f'{name} must contain {minimum}–{maximum} characters')
    return value

def digest(value): return hashlib.sha256(value.encode()).hexdigest()
def password_hash(password, salt):
    return hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1, dklen=32).hex()

def distance(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    v = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
    return 6371 * 2 * math.asin(min(1, math.sqrt(v)))

class Service:
    def __init__(self, db_path, key, clock, *, mode='development', current_offer='website'):
        if mode != 'development': raise RuntimeError('Production disabled: approved providers, age assurance and operational review are required.')
        if current_offer not in OFFER_PRICES: raise ValueError('Unknown membership offer')
        self.current_offer = current_offer
        self.db_path, self.clock, self.cipher = str(db_path), clock, Fernet(key)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with self.db() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, login TEXT UNIQUE NOT NULL, salt TEXT NOT NULL,
                password TEXT NOT NULL, recovery TEXT NOT NULL, joined INTEGER NOT NULL, trial_end INTEGER NOT NULL,
                paid_until INTEGER NOT NULL DEFAULT 0, consent_version TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS payment_events(provider TEXT NOT NULL, event_id TEXT NOT NULL,
                user_id TEXT REFERENCES users(id) ON DELETE CASCADE, amount_minor INTEGER NOT NULL,
                currency TEXT NOT NULL, access_until INTEGER NOT NULL, PRIMARY KEY(provider,event_id));
            CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
                csrf TEXT NOT NULL, expires INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS profiles(user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                alias TEXT NOT NULL, bio BLOB NOT NULL, wants BLOB NOT NULL, district TEXT NOT NULL,
                age_range TEXT NOT NULL, visible INTEGER NOT NULL DEFAULT 1);
            CREATE TABLE IF NOT EXISTS districts(code TEXT PRIMARY KEY, lat REAL NOT NULL, lon REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS conversations(id TEXT PRIMARY KEY, sender TEXT REFERENCES users(id) ON DELETE CASCADE,
                recipient TEXT REFERENCES users(id) ON DELETE CASCADE, status TEXT NOT NULL, created INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS messages(id TEXT PRIMARY KEY, conversation TEXT REFERENCES conversations(id) ON DELETE CASCADE,
                sender TEXT REFERENCES users(id) ON DELETE CASCADE, body BLOB NOT NULL, created INTEGER NOT NULL, expires INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS attachments(message_id TEXT PRIMARY KEY REFERENCES messages(id) ON DELETE CASCADE,
                data BLOB NOT NULL, width INTEGER NOT NULL, height INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS keepsakes(user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
                message_id TEXT REFERENCES messages(id) ON DELETE CASCADE, PRIMARY KEY(user_id,message_id));
            CREATE TABLE IF NOT EXISTS blocks(user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
                target TEXT REFERENCES users(id) ON DELETE CASCADE, PRIMARY KEY(user_id,target));
            CREATE TABLE IF NOT EXISTS reports(id TEXT PRIMARY KEY, reporter TEXT, target TEXT,
                reason BLOB NOT NULL, evidence BLOB, created INTEGER NOT NULL, expires INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS report_attachments(report_id TEXT PRIMARY KEY REFERENCES reports(id) ON DELETE CASCADE,
                data BLOB NOT NULL, width INTEGER NOT NULL, height INTEGER NOT NULL);
            CREATE INDEX IF NOT EXISTS message_expiry ON messages(expires);
            CREATE INDEX IF NOT EXISTS session_expiry ON sessions(expires);
            ''')
            profile_columns={r['name'] for r in db.execute('PRAGMA table_info(profiles)')}
            if 'avatar' not in profile_columns:
                db.execute("ALTER TABLE profiles ADD COLUMN avatar TEXT NOT NULL DEFAULT '{}'")
            # Remove retired body-size avatar data from old development profiles.
            for row in db.execute('SELECT user_id,avatar FROM profiles').fetchall():
                avatar=json.loads(row['avatar'])
                if 'build' in avatar or 'chest' in avatar:
                    avatar.pop('build',None);avatar.pop('chest',None)
                    db.execute('UPDATE profiles SET avatar=? WHERE user_id=?',(json.dumps(avatar),row['user_id']))
            # Additive migration: old test payments remain immediately eligible.
            columns = {r['name'] for r in db.execute('PRAGMA table_info(payment_events)')}
            if 'starts_at' not in columns:
                db.execute('ALTER TABLE payment_events ADD COLUMN starts_at INTEGER NOT NULL DEFAULT 0')
            if 'offer_code' not in columns:
                db.execute("ALTER TABLE payment_events ADD COLUMN offer_code TEXT NOT NULL DEFAULT 'launch'")
            if 'requested_start' not in columns:
                db.execute('ALTER TABLE payment_events ADD COLUMN requested_start INTEGER')
            if 'voucher_code' not in columns:
                db.execute("ALTER TABLE payment_events ADD COLUMN voucher_code TEXT NOT NULL DEFAULT ''")
            db.execute('CREATE UNIQUE INDEX IF NOT EXISTS voucher_once ON payment_events(user_id,voucher_code) WHERE voucher_code != \'\'')
            db.execute('CREATE INDEX IF NOT EXISTS payment_access ON payment_events(user_id, starts_at, access_until)')
    @contextmanager
    def db(self):
        db = sqlite3.connect(self.db_path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA secure_delete=ON')
        try:
            with db:
                yield db
        finally:
            db.close()
    def enc(self, value): return self.cipher.encrypt(value.encode())
    def dec(self, value): return self.cipher.decrypt(value).decode()
    def seed_districts(self, districts):
        """Import district centres, never home addresses; tests provide fixtures."""
        with self.db() as db:
            for code, lat, lon in districts:
                if not re.fullmatch(r'[A-Z]{1,2}\d{1,2}[A-Z]?', code): raise ValueError('Invalid outward postcode')
                if not (-90 <= lat <= 90 and -180 <= lon <= 180): raise ValueError('Invalid district centre')
                db.execute('INSERT OR REPLACE INTO districts VALUES(?,?,?)', (code,lat,lon))
    def register(self, data):
        login = text(data.get('login'), 'Login', 3, 40).lower()
        if not re.fullmatch(r'[a-z0-9_-]+', login): raise Problem(400, 'Use letters, digits, hyphens or underscores for login')
        pw = text(data.get('password'), 'Password', 12, 128)
        if data.get('adult') is not True or data.get('consent') is not True:
            raise Problem(400, 'Adult confirmation and explicit profile-data consent are required in this test service')
        profile = self.validate_profile(data)
        uid, salt, recovery = secrets.token_hex(16), secrets.token_hex(16), secrets.token_urlsafe(32)
        now = int(self.clock())
        with self.db() as db:
            try:
                db.execute('INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?)',
                    (uid,login,salt,password_hash(pw,salt),digest(recovery),now,0,0,'development-v2'))
            except sqlite3.IntegrityError: raise Problem(409,'That login is unavailable')
            db.execute('INSERT INTO profiles(user_id,alias,bio,wants,district,age_range,avatar,visible) VALUES(?,?,?,?,?,?,?,1)', (uid,*profile))
        return {'user_id':uid,'recovery_code':recovery,'payment_required':True,'development_only':True}
    def validate_profile(self, data):
        alias = text(data.get('alias'), 'Chosen name', 1, 30)
        bio = text(data.get('bio'), 'About you', 1, 300)
        wants = text(data.get('wants'), 'What you want', 1, 300)
        district = text(data.get('district'), 'Postcode district', 2, 4).upper()
        if not re.fullmatch(r'[A-Z]{1,2}\d{1,2}[A-Z]?',district): raise Problem(400,'Use an outward postcode such as GU2')
        age = data.get('age_range')
        if age not in ['18–29','30s','40s','50s','60s','70+']: raise Problem(400,'Select an adult age range')
        with self.db() as db:
            if not db.execute('SELECT 1 FROM districts WHERE code=?',(district,)).fetchone():
                raise Problem(400,'District is not in the imported postcode dataset')
        if any(key in data for key in ('avatar_url','photo_url','profile_photo','portrait')):
            raise Problem(400,'Public profiles use mouse avatars only; no photo uploads')
        try: avatar=validate_avatar(data.get('avatar'))
        except ValueError as exc: raise Problem(400,str(exc))
        return alias,self.enc(bio),self.enc(wants),district,age,json.dumps(avatar,sort_keys=True)
    def login(self, login, password):
        login = text(login,'Login',3,40).lower(); password = text(password,'Password',1,128)
        with self.db() as db:
            row = db.execute('SELECT * FROM users WHERE login=?',(login,)).fetchone()
            # Equal-cost hash even for nonexistent logins.
            actual = password_hash(password, row['salt'] if row else '00'*16)
            if not row or not hmac.compare_digest(row['password'],actual): raise Problem(401,'Incorrect login or password')
            token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
            db.execute('INSERT INTO sessions VALUES(?,?,?,?)',(digest(token),row['id'],csrf,int(self.clock())+7*DAY))
            return token, {'csrf':csrf,'user_id':row['id']}
    def authenticate(self, token, csrf=None, mutation=False):
        with self.db() as db:
            row=db.execute('SELECT * FROM sessions WHERE token=? AND expires>?',(digest(token),int(self.clock()))).fetchone()
        if not row: raise Problem(401,'Sign in required')
        if mutation and (not isinstance(csrf,str) or not hmac.compare_digest(csrf,row['csrf'])): raise Problem(403,'Invalid request token')
        return row['user_id']
    def logout(self, token):
        with self.db() as db: db.execute('DELETE FROM sessions WHERE token=?',(digest(token),))
    def recover(self, login, code, new_password):
        login=text(login,'Login',3,40).lower();code=text(code,'Recovery code',20,100);pw=text(new_password,'Password',12,128)
        with self.db() as db:
            row=db.execute('SELECT * FROM users WHERE login=?',(login,)).fetchone()
            if not row or not hmac.compare_digest(row['recovery'],digest(code)): raise Problem(401,'Recovery failed')
            new_code,salt=secrets.token_urlsafe(32),secrets.token_hex(16)
            db.execute('UPDATE users SET salt=?,password=?,recovery=? WHERE id=?',(salt,password_hash(pw,salt),digest(new_code),row['id']))
            db.execute('DELETE FROM sessions WHERE user_id=?',(row['id'],))
        return {'recovery_code':new_code}
    def membership(self, uid):
        now = int(self.clock())
        with self.db() as db:
            row = db.execute('SELECT paid_until FROM users WHERE id=?',(uid,)).fetchone()
            if not row: raise Problem(401,'Account unavailable')
            periods = db.execute('SELECT starts_at,access_until FROM payment_events WHERE user_id=? AND access_until>? ORDER BY starts_at,access_until',(uid,now)).fetchall()
        active = any(p['starts_at'] <= now < p['access_until'] for p in periods)
        start = next((p['starts_at'] for p in periods if p['starts_at'] > now),None)
        until = now
        if active:
            for p in periods:
                if p['starts_at'] <= until: until = max(until,p['access_until'])
        elif periods:
            until = periods[0]['access_until']
        else:
            until = row['paid_until']
        return {'active':active,'scheduled':not active and start is not None,'starts_at':start if not active else None,
                'access_until':until,'paid_until':row['paid_until'],'monthly_price_minor':OFFER_PRICES[self.current_offer],
                'standard_price_minor':5000,'website_price_minor':2000,'offer_code':self.current_offer,
                'currency':'GBP','automatic_renewal':False}
    def quote_month(self, uid, voucher_code='', *, offer_code=None):
        """Development quote only; not a reserved order or proof of payment."""
        offer_code = self.current_offer if offer_code is None else offer_code
        if not isinstance(offer_code,str) or offer_code not in OFFER_PRICES:
            raise Problem(400,'Unknown membership offer')
        if not isinstance(voucher_code,str) or len(voucher_code)>40:
            raise Problem(400,'Invalid invitation code')
        code=voucher_code.strip().upper()
        amount=OFFER_PRICES[offer_code];expires=None
        if code:
            campaign=VOUCHERS.get(code)
            if offer_code!='website' or not campaign or int(self.clock())>=campaign['expires_at']:
                raise Problem(400,'Invitation code unavailable or expired')
            with self.db() as db:
                if db.execute('SELECT 1 FROM payment_events WHERE user_id=? AND voucher_code=?',(uid,code)).fetchone():
                    raise Problem(409,'Invitation code already used on this account')
            amount=campaign['amount_minor'];expires=campaign['expires_at']
        return {'amount_minor':amount,'currency':'GBP','offer_code':offer_code,'voucher_code':code,
                'expires_at':expires,'automatic_renewal':False}

    def record_month_payment(self, uid, provider, event_id, amount_minor, currency, *, offer_code='launch', start_at=None, voucher_code=''):
        """Trusted development ledger; future adapters must verify a server-created order.

        The order must bind price/offer and chosen start before checkout. No public
        payment-grant endpoint exists. A later callback must use the original order
        and purchase time rather than revalidating a date against callback time.
        """
        provider=text(provider,'Provider',1,40);event_id=text(event_id,'Payment event',1,200)
        if not isinstance(offer_code,str) or offer_code not in OFFER_PRICES:
            raise Problem(400,'Unknown membership offer')
        if not isinstance(voucher_code,str) or len(voucher_code)>40:raise Problem(400,'Invalid invitation code')
        voucher_code=voucher_code.strip().upper()
        if type(amount_minor) is not int or currency!='GBP':
            raise Problem(400,'Payment does not match the confirmed GBP membership offer')
        if start_at is not None and type(start_at) is not int:
            raise Problem(400,'Choose a valid membership start time')
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            existing=db.execute('SELECT * FROM payment_events WHERE provider=? AND event_id=?',(provider,event_id)).fetchone()
            if existing:
                if (existing['user_id']!=uid or existing['amount_minor']!=amount_minor or existing['currency']!=currency
                    or existing['offer_code']!=offer_code or existing['voucher_code']!=voucher_code or (start_at is not None and existing['requested_start']!=start_at)):
                    raise Problem(409,'Payment event does not match this account or purchase')
                return {'starts_at':existing['starts_at'],'access_until':existing['access_until'],'duplicate':True}
            quote=self.quote_month(uid,voucher_code,offer_code=offer_code)
            if amount_minor!=quote['amount_minor']:raise Problem(400,'Payment does not match the confirmed GBP membership offer')
            user=db.execute('SELECT paid_until FROM users WHERE id=?',(uid,)).fetchone()
            if not user:raise Problem(404,'Account unavailable')
            now=int(self.clock())
            if start_at is not None and not now <= start_at <= now+7*DAY:
                raise Problem(400,'Start now or within seven days of purchase')
            # A repeat purchase preserves already-bought time; it never overlaps it.
            starts=max(now if start_at is None else start_at,user['paid_until'])
            until=advance_month(starts)
            db.execute('INSERT INTO payment_events(provider,event_id,user_id,amount_minor,currency,access_until,starts_at,offer_code,requested_start,voucher_code) VALUES(?,?,?,?,?,?,?,?,?,?)',
                (provider,event_id,uid,amount_minor,currency,until,starts,offer_code,start_at,voucher_code))
            db.execute('UPDATE users SET paid_until=? WHERE id=?',(until,uid))
        return {'starts_at':starts,'access_until':until,'duplicate':False}

    def active(self, uid):
        membership=self.membership(uid)
        if not membership['active']:
            raise Problem(402,'Your paid month has not started yet' if membership['scheduled'] else 'A paid month is required; renewal is manual')
    def profile(self, uid):
        with self.db() as db: p=db.execute('SELECT * FROM profiles WHERE user_id=?',(uid,)).fetchone()
        if not p: raise Problem(404,'Profile unavailable')
        return {'id':uid,'alias':p['alias'],'bio':self.dec(p['bio']),'wants':self.dec(p['wants']),
                'district':p['district'],'age_range':p['age_range'],'avatar':validate_avatar(json.loads(p['avatar'])),'visible':bool(p['visible']),'identity_verified':False,'profile_kind':'demo'}
    def edit_profile(self, uid, data):
        values=self.validate_profile(data)
        visible=data.get('visible',True)
        if not isinstance(visible,bool): raise Problem(400,'Visibility must be true or false')
        with self.db() as db: db.execute('UPDATE profiles SET alias=?,bio=?,wants=?,district=?,age_range=?,avatar=?,visible=? WHERE user_id=?',(*values,int(visible),uid))
        return self.profile(uid)
    def blocked(self, db, a, b):
        return bool(db.execute('SELECT 1 FROM blocks WHERE (user_id=? AND target=?) OR (user_id=? AND target=?)',(a,b,b,a)).fetchone())
    def discover(self, uid, district, radius=25):
        self.active(uid);district=text(district,'Postcode district',2,4).upper()
        if not isinstance(radius,(int,float)) or isinstance(radius,bool) or not math.isfinite(radius) or not 1<=radius<=200:
            raise Problem(400,'Radius must be between 1 and 200 km')
        with self.db() as db:
            centre=db.execute('SELECT lat,lon FROM districts WHERE code=?',(district,)).fetchone()
            if not centre: raise Problem(400,'District is not in the imported postcode dataset')
            rows=db.execute('''SELECT p.user_id,p.district,d.lat,d.lon FROM profiles p JOIN districts d ON p.district=d.code
                JOIN users u ON p.user_id=u.id WHERE p.visible=1 AND p.user_id!=? AND EXISTS (SELECT 1 FROM payment_events e WHERE e.user_id=u.id AND e.starts_at<=? AND e.access_until>?)''',(uid,int(self.clock()),int(self.clock()))).fetchall()
            found=[]
            for p in rows:
                km=distance(centre,(p['lat'],p['lon']))
                if km>radius or self.blocked(db,uid,p['user_id']): continue
                profile=self.profile(p['user_id'])
                # Stable decorative offset from district centre; no home/GPS data is involved.
                seed=int(hashlib.sha256(p['user_id'].encode()).hexdigest()[:8],16)
                profile.update({'district_centre':{'lat':p['lat'],'lon':p['lon']},'marker_offset':{'x':(seed%21)-10,'y':((seed//21)%21)-10},'distance_band_km':int(km//5)*5})
                found.append(profile)
        return sorted(found,key=lambda p:(p['distance_band_km'],p['id']))
    def request(self, uid, target):
        self.active(uid);self.active(target)
        if uid==target: raise Problem(400,'Choose another patron')
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            p=db.execute('SELECT visible FROM profiles WHERE user_id=?',(target,)).fetchone()
            if not p or not p['visible'] or self.blocked(db,uid,target): raise Problem(404,'Profile unavailable')
            old=db.execute('SELECT id FROM conversations WHERE (sender=? AND recipient=?) OR (sender=? AND recipient=?)',(uid,target,target,uid)).fetchone()
            if old: return {'id':old['id']}
            cid=secrets.token_hex(16);db.execute('INSERT INTO conversations VALUES(?,?,?,?,?)',(cid,uid,target,'pending',int(self.clock())))
        return {'id':cid}
    def conversation(self, db, uid, cid, *, allow_blocked=False):
        c=db.execute('SELECT * FROM conversations WHERE id=?',(cid,)).fetchone()
        if not c or uid not in (c['sender'],c['recipient']): raise Problem(404,'Conversation unavailable')
        if not allow_blocked and self.blocked(db,c['sender'],c['recipient']): raise Problem(403,'Conversation blocked')
        return c
    def accept(self, uid, cid):
        self.active(uid)
        with self.db() as db:
            c=self.conversation(db,uid,cid)
            if uid!=c['recipient']: raise Problem(403,'Only the recipient can accept')
            db.execute("UPDATE conversations SET status='accepted' WHERE id=?",(cid,))
        return {'status':'accepted'}
    def inbox(self, uid):
        with self.db() as db:
            rows=db.execute('SELECT * FROM conversations WHERE sender=? OR recipient=? ORDER BY created DESC',(uid,uid)).fetchall()
            return [{'id':c['id'],'status':c['status'],'other':c['recipient'] if c['sender']==uid else c['sender'],
                'incoming':c['recipient']==uid,
                'other_alias':db.execute('SELECT alias FROM profiles WHERE user_id=?',(c['recipient'] if c['sender']==uid else c['sender'],)).fetchone()['alias']} for c in rows if not self.blocked(db,c['sender'],c['recipient'])]
    def send(self, uid, cid, body):
        self.active(uid);body=text(body,'Message',1,2000);now=int(self.clock())
        with self.db() as db:
            c=self.conversation(db,uid,cid)
            if c['status']!='accepted': raise Problem(403,'Wait for the recipient to accept')
            mid=secrets.token_hex(16);db.execute('INSERT INTO messages VALUES(?,?,?,?,?,?)',(mid,cid,uid,self.enc(body),now,now+14*DAY))
        return {'id':mid,'expires':now+14*DAY}
    def send_image(self, uid, cid, raw):
        from .images import normalise_image
        self.active(uid)
        with self.db() as db:
            c=self.conversation(db,uid,cid)
            if c['status']!='accepted':raise Problem(403,'Wait for the recipient to accept')
        pixels,width,height=normalise_image(raw)
        encrypted=self.cipher.encrypt(pixels);now=int(self.clock());mid=secrets.token_hex(16)
        self.purge()
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            c=self.conversation(db,uid,cid)
            if c['status']!='accepted':raise Problem(403,'Wait for the recipient to accept')
            used=db.execute('SELECT coalesce(sum(length(a.data)),0) FROM attachments a JOIN messages m ON m.id=a.message_id WHERE m.sender=?',(uid,)).fetchone()[0]
            if used+len(encrypted)>100*1024*1024:raise Problem(409,'Local image storage allowance is full')
            db.execute('INSERT INTO messages VALUES(?,?,?,?,?,?)',(mid,cid,uid,self.enc(''),now,now+14*DAY))
            db.execute('INSERT INTO attachments VALUES(?,?,?,?)',(mid,encrypted,width,height))
        return {'id':mid,'expires':now+14*DAY,'image':{'url':'/api/images/'+mid,'width':width,'height':height}}
    def image(self, uid, mid):
        self.purge()
        with self.db() as db:
            m=db.execute('SELECT * FROM messages WHERE id=?',(mid,)).fetchone()
            if not m:raise Problem(404,'Image unavailable')
            self.conversation(db,uid,m['conversation'])
            if m['expires']<=self.clock() and not db.execute('SELECT 1 FROM keepsakes WHERE user_id=? AND message_id=?',(uid,mid)).fetchone():raise Problem(404,'Image expired')
            a=db.execute('SELECT data FROM attachments WHERE message_id=?',(mid,)).fetchone()
            if not a:raise Problem(404,'Image unavailable')
        return self.cipher.decrypt(a['data'])
    def image_details(self, db, mid):
        a=db.execute('SELECT width,height FROM attachments WHERE message_id=?',(mid,)).fetchone()
        return {'url':'/api/images/'+mid,'width':a['width'],'height':a['height']} if a else None

    def messages(self, uid, cid):
        self.purge()
        with self.db() as db:
            self.conversation(db,uid,cid)
            rows=db.execute('''SELECT m.*,k.message_id saved FROM messages m LEFT JOIN keepsakes k
                ON k.message_id=m.id AND k.user_id=? WHERE conversation=? AND (expires>? OR k.message_id IS NOT NULL)
                ORDER BY created,m.id''',(uid,cid,int(self.clock()))).fetchall()
            return [{'id':m['id'],'sender':m['sender'],'body':self.dec(m['body']),'expires':m['expires'],'saved':bool(m['saved']),'image':self.image_details(db,m['id'])} for m in rows]
    def keep(self, uid, mid):
        self.active(uid)
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            m=db.execute('SELECT * FROM messages WHERE id=?',(mid,)).fetchone()
            if not m: raise Problem(404,'Message unavailable')
            self.conversation(db,uid,m['conversation'])
            if db.execute('SELECT 1 FROM keepsakes WHERE user_id=? AND message_id=?',(uid,mid)).fetchone(): return {'saved':True}
            if m['expires']<=self.clock(): raise Problem(404,'Message expired')
            if db.execute('SELECT count(*) FROM keepsakes WHERE user_id=?',(uid,)).fetchone()[0]>=100: raise Problem(409,'All 100 keepsake spaces are occupied')
            db.execute('INSERT INTO keepsakes VALUES(?,?)',(uid,mid))
        return {'saved':True}
    def keepsakes(self, uid):
        with self.db() as db:
            rows=db.execute('SELECT m.* FROM messages m JOIN keepsakes k ON m.id=k.message_id WHERE k.user_id=? ORDER BY created DESC',(uid,)).fetchall()
            allowed=[]
            for m in rows:
                try: self.conversation(db,uid,m['conversation'])
                except Problem: continue
                allowed.append({'id':m['id'],'body':self.dec(m['body']),'sender':m['sender'],'image':self.image_details(db,m['id'])})
        return allowed
    def unkeep(self, uid, mid):
        with self.db() as db: db.execute('DELETE FROM keepsakes WHERE user_id=? AND message_id=?',(uid,mid))
        self.purge();return {'saved':False}
    def block(self, uid, target):
        if uid==target: raise Problem(400,'Cannot block yourself')
        with self.db() as db:
            if not db.execute('SELECT 1 FROM users WHERE id=?',(target,)).fetchone(): raise Problem(404,'Profile unavailable')
            db.execute('INSERT OR IGNORE INTO blocks VALUES(?,?)',(uid,target))
        return {'blocked':True}
    def report(self, uid, target, reason, message_id=None):
        reason=text(reason,'Reason',1,1000);evidence=None;attachment=None
        with self.db() as db:
            if not db.execute('SELECT 1 FROM users WHERE id=?',(target,)).fetchone(): raise Problem(404,'Profile unavailable')
            if message_id:
                m=db.execute('SELECT * FROM messages WHERE id=?',(message_id,)).fetchone()
                if not m: raise Problem(404,'Message unavailable')
                self.conversation(db,uid,m['conversation'],allow_blocked=True)
                if m['sender']!=target: raise Problem(400,'Reported message must belong to the reported patron')
                if m['expires']<=self.clock() and not db.execute('SELECT 1 FROM keepsakes WHERE user_id=? AND message_id=?',(uid,message_id)).fetchone(): raise Problem(404,'Message expired')
                evidence=m['body']
                attachment=db.execute('SELECT * FROM attachments WHERE message_id=?',(message_id,)).fetchone()
            rid=secrets.token_hex(16);now=int(self.clock())
            # Development retention only. Production evidence handling must be explicitly decided.
            db.execute('INSERT INTO reports VALUES(?,?,?,?,?,?,?)',(rid,uid,target,self.enc(reason),evidence,now,now+90*DAY))
            if attachment:db.execute('INSERT INTO report_attachments VALUES(?,?,?,?)',(rid,attachment['data'],attachment['width'],attachment['height']))
        return {'id':rid,'retention_days':90}
    def delete_account(self, uid):
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('DELETE FROM users WHERE id=?',(uid,))
            db.execute('UPDATE reports SET reporter=NULL WHERE reporter=?',(uid,))
            db.execute('UPDATE reports SET target=NULL WHERE target=?',(uid,))
        self.purge();return {'deleted':True,'note':'Reported evidence follows the separate development retention rule; backups are not managed by this service.'}
    def purge(self):
        with self.db() as db:
            now=int(self.clock())
            result=db.execute('DELETE FROM messages WHERE expires<=? AND NOT EXISTS(SELECT 1 FROM keepsakes WHERE message_id=messages.id)',(now,)).rowcount
            db.execute('DELETE FROM sessions WHERE expires<=?',(now,))
            db.execute('DELETE FROM reports WHERE expires<=?',(now,))
        return {'deleted_messages':result}
