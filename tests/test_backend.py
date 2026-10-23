import io,json,tempfile,unittest
from pathlib import Path
from datetime import datetime,timezone
from cryptography.fernet import Fernet
from backend.service import Service,Problem,DAY,advance_month
from backend.server import App
class CoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.now=1769853600;self.s=Service(Path(self.tmp.name)/'db.sqlite3',Fernet.generate_key(),lambda:self.now)
        self.s.seed_districts([('GU2',51.24,-.59),('GU1',51.24,-.56),('SW1A',51.50,-.14)])
        self.a=self.register('alice','GU2');self.b=self.register('bob','GU1');self.c=self.register('carol','SW1A')
    def tearDown(self):self.tmp.cleanup()
    def register(self,name,district):
        result=self.s.register(dict(login=name,password='A-long-test-passphrase',alias=name.title(),bio='Invented test adult',wants='A test conversation',district=district,age_range='40s',adult=True,consent=True))
        self.s.record_month_payment(result['user_id'],'development',name+'-first',1000,'GBP')
        return result
    def problem(self,status,fn,*args):
        with self.assertRaises(Problem) as c:fn(*args)
        self.assertEqual(c.exception.status,status)
    def conversation(self):
        cid=self.s.request(self.a['user_id'],self.b['user_id'])['id'];self.s.accept(self.b['user_id'],cid);return cid
    def test_two_adults_find_accept_and_exchange_privately(self):
        a,b=self.a['user_id'],self.b['user_id'];found=self.s.discover(a,'GU2',10)
        self.assertEqual([p['id'] for p in found],[b]);self.assertNotIn('login',found[0]);self.assertFalse(found[0]['identity_verified'])
        cid=self.s.request(a,b)['id'];self.problem(403,self.s.send,a,cid,'Not accepted');self.problem(403,self.s.accept,a,cid);self.s.accept(b,cid)
        mid=self.s.send(a,cid,'Hello from Alice')['id'];self.assertEqual(self.s.messages(b,cid)[0]['body'],'Hello from Alice');self.s.send(b,cid,'Hello back');self.assertEqual(len(self.s.messages(a,cid)),2)
        self.problem(404,self.s.messages,self.c['user_id'],cid);self.problem(404,self.s.keep,self.c['user_id'],mid)
        with self.s.db() as db:self.assertNotIn(b'Hello from Alice',db.execute('SELECT body FROM messages WHERE id=?',(mid,)).fetchone()[0])
    def test_voucher_price_expiry_single_use_and_replay(self):
        uid=self.a['user_id'];self.now=int(datetime(2026,11,30,23,59,59,tzinfo=timezone.utc).timestamp())
        q=self.s.quote_month(uid,' keele_su_10 ');self.assertEqual(q['amount_minor'],1000)
        self.assertEqual(self.s.quote_month(uid)['amount_minor'],2000)
        with self.assertRaises(Problem):self.s.record_month_payment(uid,'development','bad-discount',2000,'GBP',offer_code='website',voucher_code='KEELE_SU_10')
        paid=self.s.record_month_payment(uid,'development','voucher',1000,'GBP',offer_code='website',voucher_code='keele_su_10',start_at=self.now+7*DAY)
        self.problem(409,self.s.quote_month,uid,'KEELE_SU_10')
        self.now+=1
        self.problem(400,self.s.quote_month,self.b['user_id'],'KEELE_SU_10')
        replay=self.s.record_month_payment(uid,'development','voucher',1000,'GBP',offer_code='website',voucher_code='KEELE_SU_10')
        self.assertTrue(replay['duplicate']);self.assertEqual(paid['access_until'],replay['access_until'])
        with self.assertRaises(Problem):self.s.record_month_payment(uid,'development','voucher',2000,'GBP',offer_code='website')
    def test_voucher_rejects_unknown_stacking_and_price_tampering(self):
        uid=self.a['user_id']
        for code in ['INVALID','KEELE_SU_10,OTHER',[],1000]:
            self.problem(400,self.s.quote_month,uid,code)
        with self.assertRaises(Problem):self.s.quote_month(uid,'KEELE_SU_10',offer_code='standard')
        with self.assertRaises(Problem):self.s.record_month_payment(uid,'development','cheap',1000,'GBP',offer_code='website')
        self.assertEqual(self.s.quote_month(uid,offer_code='standard')['amount_minor'],5000)

    def test_recovery_revokes_sessions_and_rotates_code(self):
        token,session=self.s.login('alice','A-long-test-passphrase');self.problem(403,self.s.authenticate,token,'wrong',True)
        self.assertEqual(self.s.authenticate(token,session['csrf'],True),self.a['user_id'])
        self.s.recover('alice',self.a['recovery_code'],'A-new-test-passphrase');self.problem(401,self.s.authenticate,token)
        self.problem(401,self.s.recover,'alice',self.a['recovery_code'],'Another-test-passphrase');self.s.login('alice','A-new-test-passphrase')
    def test_expiry_and_individual_keepsake_visibility(self):
        cid=self.conversation();a,b=self.a['user_id'],self.b['user_id'];mid=self.s.send(a,cid,'Saved by Bob')['id'];self.s.keep(b,mid);self.now+=14*DAY
        self.assertEqual(self.s.messages(a,cid),[]);self.assertEqual(len(self.s.messages(b,cid)),1);self.s.unkeep(b,mid)
        with self.s.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],0)
    def test_100_keepsakes_and_idempotent_saving(self):
        cid=self.conversation();a=self.a['user_id'];ids=[self.s.send(a,cid,str(i))['id'] for i in range(101)]
        for mid in ids[:100]:self.s.keep(a,mid)
        self.s.keep(a,ids[0]);self.assertEqual(len(self.s.keepsakes(a)),100);self.problem(409,self.s.keep,a,ids[100]);self.s.unkeep(a,ids[0]);self.s.keep(a,ids[100])
    def test_block_stops_discovery_and_messages(self):
        cid=self.conversation();a,b=self.a['user_id'],self.b['user_id'];self.s.block(b,a);self.assertEqual(self.s.discover(a,'GU2',10),[]);self.problem(403,self.s.send,a,cid,'Blocked');self.problem(403,self.s.messages,a,cid)
    def test_reporting_still_works_after_blocking(self):
        cid=self.conversation();a,b=self.a['user_id'],self.b['user_id']
        mid=self.s.send(a,cid,'Report this')['id'];self.s.block(b,a)
        self.assertIn('id',self.s.report(b,a,'Report after blocking',mid))
    def test_paid_month_expiry_and_calendar_month(self):
        self.now=self.s.membership(self.a['user_id'])['access_until'];self.assertFalse(self.s.membership(self.a['user_id'])['active']);self.problem(402,self.s.discover,self.a['user_id'],'GU2')
        t=int(datetime(2028,1,31,10,tzinfo=timezone.utc).timestamp());self.assertEqual(datetime.fromtimestamp(advance_month(t),timezone.utc).day,29)
    def test_hidden_profiles_not_discovered(self):
        data=self.s.profile(self.b['user_id']);data['visible']=False;self.s.edit_profile(self.b['user_id'],data);self.assertEqual(self.s.discover(self.a['user_id'],'GU2',10),[])
    def test_account_deletion_cascades(self):
        cid=self.conversation();self.s.send(self.a['user_id'],cid,'Temporary');token,_=self.s.login('alice','A-long-test-passphrase');self.s.delete_account(self.a['user_id']);self.problem(401,self.s.authenticate,token);self.problem(404,self.s.messages,self.b['user_id'],cid)
        with self.s.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],0)
    def test_report_evidence_has_separate_expiry(self):
        cid=self.conversation();a,b=self.a['user_id'],self.b['user_id'];mid=self.s.send(a,cid,'Reported evidence')['id'];self.s.report(b,a,'Test report',mid);self.now+=15*DAY;self.s.purge()
        with self.s.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],0);self.assertEqual(self.s.dec(db.execute('SELECT evidence FROM reports').fetchone()[0]),'Reported evidence')
        self.now+=76*DAY;self.s.purge()
        with self.s.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM reports').fetchone()[0],0)
    def test_upfront_payment_no_free_access_and_idempotent_renewal(self):
        created=self.s.register(dict(login='unpaid',password='A-long-test-passphrase',alias='Unpaid',bio='Test adult',wants='Test hello',district='GU2',age_range='40s',adult=True,consent=True))
        uid=created['user_id'];self.assertTrue(created['payment_required']);self.assertFalse(self.s.membership(uid)['active'])
        self.problem(402,self.s.discover,uid,'GU2')
        self.problem(400,self.s.record_month_payment,uid,'development','wrong-price',999,'GBP')
        first=self.s.record_month_payment(uid,'development','month-one',1000,'GBP')
        replay=self.s.record_month_payment(uid,'development','month-one',1000,'GBP');self.assertTrue(replay['duplicate']);self.assertEqual(first['access_until'],replay['access_until'])
        self.problem(409,self.s.record_month_payment,self.a['user_id'],'development','month-one',1000,'GBP')
        second=self.s.record_month_payment(uid,'development','month-two',1000,'GBP');self.assertEqual(second['access_until'],advance_month(first['access_until']))
        self.now=second['access_until']+DAY
        renewed=self.s.record_month_payment(uid,'development','month-three',1000,'GBP');self.assertEqual(renewed['access_until'],advance_month(self.now))
    def unpaid(self, name='future'):
        return self.s.register(dict(login=name,password='A-long-test-passphrase',alias=name.title(),bio='Test adult',wants='Test hello',district='GU2',age_range='40s',adult=True,consent=True))['user_id']
    def test_launch_and_standard_offers_validate_their_own_prices(self):
        uid=self.unpaid()
        self.s.record_month_payment(uid,'development','standard',5000,'GBP',offer_code='standard')
        self.assertTrue(self.s.membership(uid)['active'])
        for amount,offer in [(1000,'standard'),(5000,'launch'),(999,'launch')]:
            with self.assertRaises(Problem) as caught:self.s.record_month_payment(uid,'development','bad-'+str(amount)+offer,amount,'GBP',offer_code=offer)
            self.assertEqual(caught.exception.status,400)
        with self.assertRaises(Problem):self.s.record_month_payment(uid,'development','unknown',1000,'GBP',offer_code='client-discount')
    def test_deferred_month_blocks_discovery_until_exact_start(self):
        uid=self.unpaid();start=self.now+7*DAY
        purchase=self.s.record_month_payment(uid,'development','later',1000,'GBP',start_at=start)
        self.assertEqual(purchase['access_until'],advance_month(start))
        membership=self.s.membership(uid);self.assertFalse(membership['active']);self.assertTrue(membership['scheduled'])
        self.problem(402,self.s.discover,uid,'GU2')
        self.assertNotIn(uid,[p['id'] for p in self.s.discover(self.a['user_id'],'GU2')])
        self.now=start-1;self.assertFalse(self.s.membership(uid)['active'])
        self.now=start;self.assertTrue(self.s.membership(uid)['active'])
        self.assertIn(uid,[p['id'] for p in self.s.discover(self.a['user_id'],'GU2')])
        self.now=purchase['access_until'];self.assertFalse(self.s.membership(uid)['active'])
    def test_deferred_purchase_replay_does_not_move_dates(self):
        uid=self.unpaid();start=self.now+DAY
        first=self.s.record_month_payment(uid,'development','replay-later',1000,'GBP',start_at=start)
        self.now+=10*DAY
        replay=self.s.record_month_payment(uid,'development','replay-later',1000,'GBP',start_at=start)
        self.assertTrue(replay['duplicate']);self.assertEqual(replay['access_until'],first['access_until'])
        with self.assertRaises(Problem) as caught:self.s.record_month_payment(uid,'development','replay-later',1000,'GBP',start_at=start+DAY)
        self.assertEqual(caught.exception.status,409)
    def test_start_window_and_renewal_gap_are_enforced(self):
        uid=self.unpaid()
        for start in (self.now-1,self.now+7*DAY+1,True,1.5):
            with self.assertRaises(Problem):self.s.record_month_payment(uid,'development','invalid-'+str(start),1000,'GBP',start_at=start)
        end=self.s.membership(self.a['user_id'])['access_until'];self.now=end-2*DAY;start=end+3*DAY
        purchase=self.s.record_month_payment(self.a['user_id'],'development','gap',5000,'GBP',offer_code='standard',start_at=start)
        self.assertEqual(purchase['starts_at'],start)
        self.assertEqual(self.s.membership(self.a['user_id'])['access_until'],end)
        self.now=end;self.assertFalse(self.s.membership(self.a['user_id'])['active']);self.assertTrue(self.s.membership(self.a['user_id'])['scheduled'])
        self.now=start;self.assertTrue(self.s.membership(self.a['user_id'])['active'])
    def test_early_renewal_preserves_time_and_original_requested_start(self):
        uid=self.a['user_id'];end=self.s.membership(uid)['access_until'];requested=self.now+DAY
        first=self.s.record_month_payment(uid,'development','early',1000,'GBP',start_at=requested)
        replay=self.s.record_month_payment(uid,'development','early',1000,'GBP',start_at=requested)
        self.assertEqual(first['starts_at'],end);self.assertEqual(first['access_until'],advance_month(end));self.assertTrue(replay['duplicate'])
        self.assertEqual(self.s.membership(uid)['access_until'],first['access_until'])
    def test_old_payment_schema_is_migrated_without_losing_access(self):
        key=Fernet.generate_key();path=Path(self.tmp.name)/'legacy.sqlite3';service=Service(path,key,lambda:self.now)
        service.seed_districts([('GU2',51.24,-.59)])
        uid=service.register(dict(login='legacy',password='A-long-test-passphrase',alias='Legacy',bio='Test adult',wants='Test hello',district='GU2',age_range='40s',adult=True,consent=True))['user_id']
        until=advance_month(self.now)
        with service.db() as db:
            db.execute('DROP TABLE payment_events')
            db.execute('CREATE TABLE payment_events(provider TEXT,event_id TEXT,user_id TEXT,amount_minor INTEGER,currency TEXT,access_until INTEGER,PRIMARY KEY(provider,event_id))')
            db.execute('INSERT INTO payment_events VALUES(?,?,?,?,?,?)',('development','legacy-event',uid,1000,'GBP',until))
            db.execute('UPDATE users SET paid_until=? WHERE id=?',(until,uid))
        reopened=Service(path,key,lambda:self.now)
        self.assertTrue(reopened.membership(uid)['active'])
        self.assertTrue(reopened.record_month_payment(uid,'development','legacy-event',1000,'GBP')['duplicate'])
    def test_mouse_avatar_is_persisted_and_discovered_without_photo_urls(self):
        uid=self.a['user_id'];data=self.s.profile(uid)
        self.assertIn('avatar',data)
        data['avatar'].update(hair='crew',face='rugged',facialHair='beard',build='athletic',chest='flat',outfit='leather',accessory='glasses')
        updated=self.s.edit_profile(uid,data)
        self.assertEqual(updated['avatar']['hair'],'crew')
        self.assertEqual(updated['avatar']['face'],'rugged')
        self.assertEqual(updated['avatar']['facialHair'],'beard')
        self.assertEqual(updated['avatar']['outfit'],'leather')
        found=next(p for p in self.s.discover(self.b['user_id'],'GU1',10) if p['id']==uid)
        self.assertEqual(found['avatar'],updated['avatar']);self.assertNotIn('photo_url',found)
        for bad in ({'hair':'https://example.invalid/photo.jpg'},{'image':'data:image/svg+xml,bad'},'<svg onload=bad>'):
            data['avatar']=bad
            self.problem(400,self.s.edit_profile,uid,data)
        data=self.s.profile(uid);data['photo_url']='https://example.invalid/face.jpg'
        self.problem(400,self.s.edit_profile,uid,data)
    def test_production_disabled(self):
        with self.assertRaises(RuntimeError):Service(Path(self.tmp.name)/'prod.sqlite3',Fernet.generate_key(),lambda:self.now,mode='production')
    def http(self,method,path,data=None,cookie='',csrf='',origin='http://127.0.0.1:8080',host='127.0.0.1:8080'):
        raw=json.dumps(data).encode() if data is not None else b'';out={};env=dict(REQUEST_METHOD=method,PATH_INFO=path,HTTP_HOST=host,HTTP_ORIGIN=origin,CONTENT_TYPE='application/json',CONTENT_LENGTH=str(len(raw)),REMOTE_ADDR='127.0.0.1',HTTP_COOKIE=cookie,HTTP_X_CSRF_TOKEN=csrf);env['wsgi.input']=io.BytesIO(raw)
        body=b''.join(self.app(env,lambda status,headers:out.update(status=int(status[:3]),headers=dict(headers))));return out,json.loads(body)
    def test_http_cookie_csrf_origin_and_no_payment_override(self):
        self.app=App(self.s);res,data=self.http('POST','/api/login',dict(login='alice',password='A-long-test-passphrase'));self.assertEqual(res['status'],200);cookie=res['headers']['Set-Cookie'].split(';')[0];self.assertIn('HttpOnly',res['headers']['Set-Cookie'])
        res,_=self.http('POST','/api/discover',{'district':'GU2'},cookie=cookie);self.assertEqual(res['status'],403)
        res,_=self.http('POST','/api/discover',{'district':'GU2'},cookie=cookie,csrf=data['csrf']);self.assertEqual(res['status'],200)
        res,_=self.http('POST','/api/discover',{'district':'GU2'},cookie=cookie,csrf=data['csrf'],origin='https://attacker.invalid');self.assertEqual(res['status'],403)
        res,_=self.http('GET','/api/health',host='attacker.invalid');self.assertEqual(res['status'],403)
        for path in ['/api/pay','/api/age-verified']:
            res,_=self.http('POST',path,{},cookie=cookie,csrf=data['csrf']);self.assertEqual(res['status'],404)
if __name__=='__main__':unittest.main()
