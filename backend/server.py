"""Loopback-only development API; deliberately cannot run as production."""
import argparse, json, os, re, secrets, threading, time
from pathlib import Path
from collections import defaultdict, deque
from http.cookies import SimpleCookie
from wsgiref.simple_server import make_server, WSGIRequestHandler
from .service import Service, Problem, digest, OFFER_PRICES

class App:
    def __init__(self,service,origin='http://127.0.0.1:8080'):
        self.web_root=Path(__file__).resolve().parent.parent
        self.service,self.origin=service,origin;self.attempts=defaultdict(deque);self.lock=threading.Lock()
    def throttle(self,peer,kind,limit):
        now=time.monotonic()
        with self.lock:
            for key in list(self.attempts):
                q=self.attempts[key]
                while q and q[0]<now-3600:q.popleft()
                if not q:del self.attempts[key]
            q=self.attempts[(peer,kind)]
            if len(q)>=limit:raise Problem(429,'Too many attempts; try later')
            q.append(now)
    def __call__(self,env,start):
        headers=[]
        try:
            method,path=env['REQUEST_METHOD'],env.get('PATH_INFO','')
            if env.get('HTTP_HOST')!=self.origin.split('://',1)[1]:raise Problem(403,'Unexpected host')
            if method not in ('GET','POST','DELETE'):raise Problem(405,'Method not allowed')
            # Explicit assets only. Never expose source, runtime databases, keys or arbitrary paths.
            assets={'/chemistry.html':('chemistry.html','text/html'),'/chemistry.css':('chemistry.css','text/css'),'/chemistry.js':('chemistry.js','text/javascript'),'/assets/chemistry-lagoon.webp':('assets/chemistry-lagoon.webp','image/webp'),'/assets/chemistry-woodland.webp':('assets/chemistry-woodland.webp','image/webp'),'/':('index.html','text/html'),'/index.html':('index.html','text/html'),
                '/members.html':('members.html','text/html'),'/members.js':('members.js','text/javascript'),
                '/members.css':('members.css','text/css'),'/app.js':('app.js','text/javascript'),'/mouse-avatar.js':('mouse-avatar.js','text/javascript'),
                '/demo-atlas-data.js':('demo-atlas-data.js','text/javascript'),'/demo-atlas.js':('demo-atlas.js','text/javascript'),'/map-geography.js':('map-geography.js','text/javascript'),'/map-layout.js':('map-layout.js','text/javascript'),'/map-zoom.js':('map-zoom.js','text/javascript'),'/style.css':('style.css','text/css'),'/assets/anony-mouses-masthead.png':('assets/anony-mouses-masthead.png','image/png')}
            if method=='GET' and path in assets:
                filename,mime=assets[path];body=(self.web_root/filename).read_bytes()
                start('200 OK',[('Content-Type',mime),('Content-Length',str(len(body))),('Cache-Control','no-store'),
                    ('X-Content-Type-Options','nosniff'),('Referrer-Policy','no-referrer'),
                    ('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' blob:; connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'")])
                return [body]
            if not path.startswith('/api/'):raise Problem(404,'Page unavailable')
            if method!='GET' and env.get('HTTP_ORIGIN') not in (None,self.origin):raise Problem(403,'Unexpected origin')
            image_upload=method=='POST' and re.fullmatch(r'/api/conversations/([a-f0-9]{32})/images',path)
            cookies=SimpleCookie();cookies.load(env.get('HTTP_COOKIE',''))
            token=cookies['am_session'].value if 'am_session' in cookies else ''
            public=path in ['/api/register','/api/login','/api/recover','/api/health','/api/districts']
            uid=None if public else self.service.authenticate(token,env.get('HTTP_X_CSRF_TOKEN'),method!='GET')
            data={};raw=None
            if image_upload:
                from .images import MAX_UPLOAD
                self.throttle(uid,'image',60)
                if env.get('CONTENT_TYPE','').split(';')[0] not in ('image/jpeg','image/png','image/webp'):raise Problem(415,'Choose JPG, PNG or WebP')
                try:length=int(env.get('CONTENT_LENGTH') or '0')
                except ValueError:raise Problem(400,'Invalid request size')
                if not 0<length<=MAX_UPLOAD:raise Problem(413,'Choose an image up to 5 MB')
                raw=env['wsgi.input'].read(length)
                if len(raw)!=length:raise Problem(400,'Incomplete image upload')
            elif method=='POST':
                if env.get('CONTENT_TYPE','').split(';')[0]!='application/json':raise Problem(415,'Use application/json')
                try:length=int(env.get('CONTENT_LENGTH') or '0')
                except ValueError:raise Problem(400,'Invalid request size')
                if not 0<length<=16384:raise Problem(413,'Request too large or empty')
                try:data=json.loads(env['wsgi.input'].read(length))
                except (ValueError,UnicodeDecodeError):raise Problem(400,'Invalid JSON')
                if not isinstance(data,dict):raise Problem(400,'JSON object required')
            peer=env.get('REMOTE_ADDR','unknown');s=self.service
            if (m:=re.fullmatch(r'/api/images/([a-f0-9]{32})',path)) and method=='GET':
                body=s.image(uid,m[1])
                start('200 OK',[('Content-Type','image/jpeg'),('Content-Length',str(len(body))),
                    ('Cache-Control','private, no-store'),('Pragma','no-cache'),('X-Content-Type-Options','nosniff'),
                    ('Content-Disposition','inline; filename="image.jpg"'),('Referrer-Policy','no-referrer'),
                    ('Content-Security-Policy',"default-src 'none'; frame-ancestors 'none'")]);return [body]
            if image_upload:result=s.send_image(uid,image_upload[1],raw)
            elif path=='/api/health' and method=='GET':result={'status':'local-development','production_enabled':False}
            elif path=='/api/districts' and method=='GET':
                with s.db() as db:result=[dict(row) for row in db.execute('SELECT code,lat,lon FROM districts ORDER BY code')]
            elif path=='/api/quote' and method=='POST':self.throttle(uid,'quote',30);result=s.quote_month(uid,data.get('voucher_code',''))
            elif path=='/api/register' and method=='POST':self.throttle(peer,'register',10);result=s.register(data)
            elif path=='/api/login' and method=='POST':
                self.throttle(peer,'login',30);remember=data.get('remember',False)
                token,result=s.login(data.get('login'),data.get('password'),remember)
                cookie=f'am_session={token}; Path=/api; HttpOnly; SameSite=Strict'
                if remember:cookie+='; Max-Age=2592000'
                if self.origin.startswith('https://'):cookie+='; Secure'
                headers.append(('Set-Cookie',cookie))
            elif path=='/api/recover' and method=='POST':self.throttle(peer,'recover',10);result=s.recover(data.get('login'),data.get('recovery_code'),data.get('password'))
            elif path=='/api/session' and method=='GET':
                with s.db() as db:row=db.execute('SELECT csrf FROM sessions WHERE token=?',(digest(token),)).fetchone()
                result={'csrf':row['csrf'],'profile':s.profile(uid),'membership':s.membership(uid)}
            elif path=='/api/logout' and method=='POST':
                s.logout(token);headers.append(('Set-Cookie','am_session=; Path=/api; HttpOnly; SameSite=Strict; Max-Age=0'));result={'logged_out':True}
            elif path=='/api/profile' and method=='GET':result=s.profile(uid)
            elif path=='/api/profile' and method=='POST':result=s.edit_profile(uid,data)
            elif path=='/api/discover' and method=='POST':result=s.discover(uid,data.get('district'),data.get('radius_km',25))
            elif path=='/api/conversations' and method=='GET':result=s.inbox(uid)
            elif path=='/api/conversations' and method=='POST':result=s.request(uid,data.get('target'))
            elif (m:=re.fullmatch(r'/api/conversations/([a-f0-9]{32})/accept',path)) and method=='POST':result=s.accept(uid,m[1])
            elif (m:=re.fullmatch(r'/api/conversations/([a-f0-9]{32})/messages',path)) and method=='GET':result=s.messages(uid,m[1])
            elif (m:=re.fullmatch(r'/api/conversations/([a-f0-9]{32})/messages',path)) and method=='POST':self.throttle(uid,'send',300);result=s.send(uid,m[1],data.get('body'))
            elif path=='/api/keepsakes' and method=='GET':result=s.keepsakes(uid)
            elif (m:=re.fullmatch(r'/api/keepsakes/([a-f0-9]{32})',path)) and method=='POST':result=s.keep(uid,m[1])
            elif (m:=re.fullmatch(r'/api/keepsakes/([a-f0-9]{32})',path)) and method=='DELETE':result=s.unkeep(uid,m[1])
            elif path=='/api/block' and method=='POST':result=s.block(uid,data.get('target'))
            elif path=='/api/report' and method=='POST':result=s.report(uid,data.get('target'),data.get('reason'),data.get('message_id'))
            elif path=='/api/account' and method=='DELETE':result=s.delete_account(uid)
            else:raise Problem(404,'Endpoint unavailable')
            status=200
        except Problem as e:status,result=e.status,{'error':e.message}
        except Exception:status,result=500,{'error':'Local service error'}
        body=json.dumps(result,ensure_ascii=False).encode()
        names={200:'OK',400:'Bad Request',401:'Unauthorized',402:'Payment Required',403:'Forbidden',404:'Not Found',405:'Method Not Allowed',409:'Conflict',413:'Content Too Large',415:'Unsupported Media Type',429:'Too Many Requests',500:'Internal Server Error'}
        start(f'{status} {names[status]}',[('Content-Type','application/json; charset=utf-8'),('Content-Length',str(len(body))),('Cache-Control','no-store'),('X-Content-Type-Options','nosniff'),('Content-Security-Policy',"default-src 'none'; frame-ancestors 'none'"),*headers]);return [body]
class QuietHandler(WSGIRequestHandler):
    def log_message(self,*args):pass

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',default='runtime/anony-mouse.sqlite3');p.add_argument('--port',type=int,default=8080);p.add_argument('--purge',action='store_true');p.add_argument('--seed-test-districts',action='store_true');p.add_argument('--grant-test-month',metavar='LOGIN',help='Operator-only fictional monthly payment fixture; no money moves');p.add_argument('--voucher',default='',help='Development invitation code');p.add_argument('--offer',choices=['website','launch','standard'],default='website');p.add_argument('--start-in-days',type=int,choices=range(8),default=0);args=p.parse_args()
    key=os.environ.get('ANONY_MOUSE_DATA_KEY')
    if not key:raise SystemExit('Set ANONY_MOUSE_DATA_KEY through your environment; never commit it.')
    s=Service(args.db,key,time.time,current_offer=args.offer)
    if args.seed_test_districts:s.seed_districts([('GU2',51.24,-.59),('GU1',51.24,-.56),('SW1A',51.50,-.14)])
    if args.purge:print(s.purge());return
    if args.grant_test_month:
        with s.db() as db:row=db.execute('SELECT id FROM users WHERE login=?',(args.grant_test_month.strip().lower(),)).fetchone()
        if not row:raise SystemExit('Test login not found')
        quote=s.quote_month(row['id'],args.voucher,offer_code=args.offer)
        print(s.record_month_payment(row['id'],'development',secrets.token_hex(16),quote['amount_minor'],'GBP',offer_code=args.offer,voucher_code=quote['voucher_code'],start_at=int(time.time())+args.start_in_days*86400 if args.start_in_days else None));return
    origin=f'http://127.0.0.1:{args.port}';print(f'Local member lounge: {origin}/members.html. Fictional test adults only; production disabled.')
    with make_server('127.0.0.1',args.port,App(s,origin),handler_class=QuietHandler) as server:server.serve_forever()
if __name__=='__main__':main()
