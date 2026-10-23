import tempfile
import unittest
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from cryptography.fernet import Fernet
from backend.service import Service,Problem,DAY
from support import service_for_test

class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.key=Fernet.generate_key();self.now=1791980000
        self.s=service_for_test(self,Path(self.tmp.name)/'db',self.key,lambda:self.now)
        self.s.seed_districts([('GU2',51.24,-.59),('GU1',51.24,-.56),('M1',53.47,-2.24)])
        self.a=self.user('alice','GU2');self.b=self.user('bob','GU1');self.c=self.user('carol','M1')
    def user(self,name,district):
        uid=self.s.register(dict(login=name,password='Long-test-password',alias=name,bio='Invented adult',wants='Test conversation',district=district,age_range='40s',adult=True,consent=True))['user_id']
        self.s.record_month_payment(uid,'development',name,2000,'GBP',offer_code='website')
        return uid
    def problem(self,code,fn,*args,**kwargs):
        with self.assertRaises(Problem) as caught:fn(*args,**kwargs)
        self.assertEqual(caught.exception.status,code)
    def test_discovery_pages_filter_before_limit_and_do_not_repeat(self):
        ids={self.b}
        for i in range(5):ids.add(self.user('mouse'+str(i),'GU1'))
        self.s.edit_profile(self.b,{**self.s.profile(self.b),'visible':False});ids.remove(self.b)
        blocked=next(iter(ids));self.s.block(self.a,blocked);ids.remove(blocked)
        seen=[];cursor=None
        while True:
            page=self.s.discover_page(self.a,'GU2',10,limit=2,cursor=cursor)
            seen.extend(p['id'] for p in page['items']);cursor=page['next_cursor']
            self.assertTrue(all(p['distance_band_km']<=10 for p in page['items']))
            if cursor is None:break
        self.assertEqual(set(seen),ids);self.assertEqual(len(seen),len(ids));self.assertNotIn(self.c,seen)
        page=self.s.discover_page(self.a,'GU2',10,limit=1)
        self.problem(400,self.s.discover_page,self.a,'GU1',10,cursor=page['next_cursor'])
        self.problem(400,self.s.discover_page,self.a,'GU2',limit=True)
    def test_message_pages_ties_access_expiry_and_keepsakes(self):
        cid=self.s.request(self.a,self.b)['id'];self.s.accept(self.b,cid)
        ids=[self.s.send(self.a,cid,str(i))['id'] for i in range(7)]
        page=self.s.messages_page(self.b,cid,limit=2);seen=[];cursor=page['next_cursor']
        seen.extend(m['id'] for m in page['items'])
        while cursor:
            page=self.s.messages_page(self.b,cid,limit=2,cursor=cursor);seen.extend(m['id'] for m in page['items']);cursor=page['next_cursor']
        self.assertEqual(set(seen),set(ids));self.assertEqual(len(seen),7)
        self.problem(404,self.s.messages_page,self.c,cid,limit=2)
        self.s.keep(self.b,ids[0]);self.now+=14*DAY
        self.assertEqual(self.s.messages_page(self.a,cid)['items'],[])
        self.assertEqual([m['id'] for m in self.s.messages_page(self.b,cid)['items']],[ids[0]])
        with self.s.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],7)
        self.assertEqual(self.s.purge(limit=2)['deleted_messages'],2)
        self.assertEqual(self.s.purge(limit=2)['deleted_messages'],2)
        self.assertEqual(self.s.purge(limit=2)['deleted_messages'],2)
        self.assertEqual(self.s.purge(limit=2)['deleted_messages'],0)
    def test_inbox_paging_blocks_hidden_pairs(self):
        for target in (self.b,self.c):self.s.request(self.a,target)
        first=self.s.inbox_page(self.a,limit=1);second=self.s.inbox_page(self.a,limit=1,cursor=first['next_cursor'])
        self.assertNotEqual(first['items'][0]['id'],second['items'][0]['id']);self.assertIsNone(second['next_cursor'])
        self.s.block(self.b,self.a)
        self.assertEqual([c['other'] for c in self.s.inbox_page(self.a)['items']],[self.c])
        self.problem(400,self.s.inbox_page,self.a,cursor='bogus')
    def test_independent_instances_share_rate_limits_without_storing_peer(self):
        other=Service(self.s.db_path,self.key,lambda:self.now);self.addCleanup(other.close)
        self.s.throttle('198.51.100.4','login',2);other.throttle('198.51.100.4','login',2)
        self.problem(429,self.s.throttle,'198.51.100.4','login',2)
        self.s.throttle('198.51.100.4','register',2)
        with self.s.db() as db:self.assertTrue(all('198.51.100.4' not in row['key'] for row in db.execute('SELECT key FROM rate_limits')))
        self.now+=3600;other.throttle('198.51.100.4','login',2)
    def test_concurrent_payment_replay_and_keepsake_quota(self):
        def pay(_):return self.s.record_month_payment(self.a,'development','same-concurrent-event',2000,'GBP',offer_code='website')
        with ThreadPoolExecutor(max_workers=4) as pool:payments=list(pool.map(pay,range(4)))
        self.assertEqual(sum(not p['duplicate'] for p in payments),1)
        self.assertEqual(len({p['access_until'] for p in payments}),1)
        cid=self.s.request(self.a,self.b)['id'];self.s.accept(self.b,cid)
        for i in range(99):self.s.keep(self.b,self.s.send(self.a,cid,str(i))['id'])
        ids=[self.s.send(self.a,cid,'Quota race')['id'] for _ in range(4)]
        def keep(mid):
            try:self.s.keep(self.b,mid);return 200
            except Problem as exc:return exc.status
        with ThreadPoolExecutor(max_workers=4) as pool:outcomes=list(pool.map(keep,ids))
        self.assertEqual(outcomes.count(200),1);self.assertEqual(outcomes.count(409),3)
        self.assertEqual(len(self.s.keepsakes(self.b)),100)
    def test_migrations_are_repeatable_and_data_survives_reopen(self):
        other=Service(self.s.db_path,self.key,lambda:self.now);self.addCleanup(other.close)
        self.assertEqual(other.profile(self.a)['alias'],'alice')
        with other.db() as db:
            versions=[r['version'] for r in db.execute('SELECT version FROM schema_migrations')]
            self.assertEqual(len(versions),len(set(versions)))
            self.assertTrue({1,2,3,5}.issubset(versions))

if __name__=='__main__':unittest.main()
