from support import service_for_test
"""Exercise the member journey through HTTP, including cookies and isolation."""
import json
import tempfile
import threading
import unittest
from http.cookiejar import CookieJar
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import build_opener, HTTPCookieProcessor, Request
from wsgiref.simple_server import make_server
from cryptography.fernet import Fernet
from backend.server import App, QuietHandler
from backend.service import Service

class MemberHTTPTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.service = service_for_test(self,Path(self.tmp.name)/'test.sqlite3', Fernet.generate_key(), lambda: 1791980000)
        self.service.seed_districts([('GU2',51.24,-.59),('GU1',51.24,-.56)])
        self.server = make_server('127.0.0.1',0,lambda env,start: self.app(env,start),handler_class=QuietHandler)
        self.origin = 'http://127.0.0.1:' + str(self.server.server_port)
        self.app = App(self.service,self.origin)
        self.thread = threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.clients = [build_opener(HTTPCookieProcessor(CookieJar())) for _ in range(3)]
    def tearDown(self):
        self.server.shutdown(); self.thread.join(); self.server.server_close(); self.tmp.cleanup()
    def request(self,client,path,method='GET',data=None,csrf=None):
        headers={'Origin':self.origin}
        if data is not None: headers['Content-Type']='application/json'
        if csrf: headers['X-CSRF-Token']=csrf
        req=Request(self.origin+path,json.dumps(data).encode() if data is not None else None,headers,method=method)
        try: res=client.open(req)
        except HTTPError as e: res=e
        with res:
            body=res.read()
            return res.status, json.loads(body) if 'application/json' in res.headers.get('Content-Type','') else body, res.headers
    def create(self,client,name,district):
        payload=dict(login=name,password='Invented-test-password',alias=name.title(),bio='Invented adult',wants='A test hello',district=district,age_range='40s',adult=True,consent=True)
        code,created,_=self.request(client,'/api/register','POST',payload);self.assertEqual(code,200)
        self.assertTrue(created['payment_required'])
        self.service.record_month_payment(created['user_id'],'development',name+'-fixture',1000,'GBP')
        code,_,headers=self.request(client,'/api/login','POST',dict(login=name,password=payload['password']));self.assertEqual(code,200)
        self.assertIn('HttpOnly',headers['Set-Cookie'])
        code,session,_=self.request(client,'/api/session');self.assertEqual(code,200)
        return created['user_id'],session['csrf']
    def test_browser_contract_end_to_end(self):
        alice,bob,stranger=self.clients
        aid,ac=self.create(alice,'alice','GU2');bid,bc=self.create(bob,'bob','GU1');_,cc=self.create(stranger,'carol','GU1')
        code,found,_=self.request(alice,'/api/discover','POST',dict(district='GU2',radius_km=10),ac)
        self.assertEqual(code,200);self.assertIn(bid,[p['id'] for p in found]);self.assertNotIn('login',found[0])
        code,result,_=self.request(alice,'/api/conversations','POST',dict(target=bid),ac);self.assertEqual(code,200);cid=result['id']
        code,inbox,_=self.request(bob,'/api/conversations');self.assertEqual(inbox[0]['other_alias'],'Alice');self.assertTrue(inbox[0]['incoming'])
        self.assertEqual(self.request(alice,f'/api/conversations/{cid}/messages','POST',{'body':'Too soon'},ac)[0],403)
        self.assertEqual(self.request(bob,f'/api/conversations/{cid}/accept','POST',{},bc)[0],200)
        code,sent,_=self.request(alice,f'/api/conversations/{cid}/messages','POST',{'body':'Hello from the lounge'},ac);self.assertEqual(code,200)
        code,messages,_=self.request(bob,f'/api/conversations/{cid}/messages');self.assertEqual(messages[0]['body'],'Hello from the lounge')
        self.assertEqual(self.request(stranger,f'/api/conversations/{cid}/messages')[0],404)
        mid=sent['id'];self.assertEqual(self.request(bob,'/api/keepsakes/'+mid,'POST',{},bc)[0],200)
        self.assertEqual(len(self.request(bob,'/api/keepsakes')[1]),1)
        self.assertEqual(self.request(bob,'/api/keepsakes/'+mid,'DELETE',csrf=bc)[0],200)
        self.assertEqual(self.request(bob,'/api/block','POST',dict(target=aid),bc)[0],200)
        self.assertEqual(self.request(alice,f'/api/conversations/{cid}/messages','POST',{'body':'Blocked'},ac)[0],403)
        self.assertEqual(self.request(bob,'/api/report','POST',dict(target=aid,reason='Fictional concern',message_id=mid),bc)[0],200)
        self.assertEqual(self.request(alice,'/api/logout','POST',{},ac)[0],200)
        self.assertEqual(self.request(alice,'/api/session')[0],401)
    def test_opt_in_cookie_restores_access_and_signout_forgets_it(self):
        client=self.clients[0]
        self.create(client,'alice','GU2')
        credentials=dict(login='alice',password='Invented-test-password')
        _,_,headers=self.request(client,'/api/login','POST',credentials)
        self.assertNotIn('Max-Age',headers['Set-Cookie'])
        code,_,headers=self.request(client,'/api/login','POST',{**credentials,'remember':True})
        self.assertEqual(code,200)
        self.assertIn('Max-Age=2592000',headers['Set-Cookie'])
        self.assertIn('HttpOnly',headers['Set-Cookie']);self.assertIn('SameSite=Strict',headers['Set-Cookie'])
        code,session,_=self.request(client,'/api/session');self.assertEqual(code,200)
        self.assertEqual(session['profile']['alias'],'Alice')
        _,_,headers=self.request(client,'/api/logout','POST',{},session['csrf'])
        self.assertIn('Max-Age=0',headers['Set-Cookie'])
        self.assertEqual(self.request(client,'/api/session')[0],401)
        self.assertEqual(self.request(client,'/api/login','POST',{**credentials,'remember':'false'})[0],400)

    def test_assets_are_allowlisted_and_no_secrets_are_served(self):
        client=self.clients[0]
        for path in ['/members.html','/members.js','/members.css','/style.css','/assets/anony-mouses-masthead.png']:
            code,body,headers=self.request(client,path);self.assertEqual(code,200);self.assertTrue(body)
            self.assertIn("frame-ancestors 'none'",headers['Content-Security-Policy'])
        for path in ['/runtime/test.sqlite3','/.git/config','/backend/service.py','/../README.md','/%2e%2e/README.md']:
            self.assertEqual(self.request(client,path)[0],404)
        self.assertEqual(self.request(client,'/api/districts')[1][0]['code'],'GU1')

if __name__=='__main__':unittest.main()
