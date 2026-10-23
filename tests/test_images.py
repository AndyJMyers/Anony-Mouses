from support import service_for_test
import io
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from cryptography.fernet import Fernet
from backend.service import Service,Problem,DAY
from backend.server import App
from backend.images import normalise_image,MAX_UPLOAD

def picture(metadata=True):
    out=io.BytesIO();im=Image.new('RGB',(80,50),'purple');info=PngInfo()
    if metadata:info.add_text('GPS','SECRET-GPS-METADATA');info.add_text('Author','ORIGINAL-FILENAME.jpg')
    im.save(out,format='PNG',pnginfo=info);return out.getvalue()

class ImageTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.now=1791980000
        self.s=service_for_test(self,Path(self.tmp.name)/'db',Fernet.generate_key(),lambda:self.now)
        self.s.seed_districts([('GU2',51.24,-.59)])
        self.users=[]
        for name in ['alice','bob','carol']:
            uid=self.s.register(dict(login=name,password='A-test-password-long',alias=name,bio='Invented test adult',wants='Test pictures',district='GU2',age_range='40s',adult=True,consent=True))['user_id']
            self.s.record_month_payment(uid,'development',name,1000,'GBP');self.users.append(uid)
        self.a,self.b,self.c=self.users
        self.cid=self.s.request(self.a,self.b)['id']
    def tearDown(self):self.tmp.cleanup()
    def problem(self,status,fn,*args):
        with self.assertRaises(Problem) as c:fn(*args)
        self.assertEqual(c.exception.status,status)
    def send(self):
        self.s.accept(self.b,self.cid);return self.s.send_image(self.a,self.cid,picture())['id']
    def test_metadata_and_orientation_are_normalised(self):
        clean,w,h=normalise_image(picture());self.assertEqual((w,h),(80,50))
        self.assertNotIn(b'SECRET-GPS',clean);self.assertNotIn(b'ORIGINAL-FILENAME',clean)
        with Image.open(io.BytesIO(clean)) as im:self.assertEqual(im.format,'JPEG');self.assertFalse(im.getexif());self.assertNotIn('icc_profile',im.info)
        im=Image.new('RGB',(80,50),'blue');exif=Image.Exif();exif[274]=6;exif[270]='Secret description'
        out=io.BytesIO();im.save(out,'JPEG',exif=exif)
        clean,w,h=normalise_image(out.getvalue()+b'TRAILING-SECRET');self.assertEqual((w,h),(50,80));self.assertNotIn(b'Secret description',clean);self.assertNotIn(b'TRAILING-SECRET',clean)
    def test_invalid_oversized_and_animated_images_are_rejected(self):
        self.problem(400,normalise_image,b'<svg><script>alert(1)</script></svg>')
        self.problem(413,normalise_image,b'x'*(MAX_UPLOAD+1))
        out=io.BytesIO();Image.new('RGB',(4001,3000)).save(out,'PNG');self.problem(413,normalise_image,out.getvalue())
        out=io.BytesIO();Image.new('RGB',(10,10),'red').save(out,'PNG',save_all=True,append_images=[Image.new('RGB',(10,10),'blue')],duration=100,loop=0)
        self.problem(400,normalise_image,out.getvalue())
    def test_acceptance_access_and_blocking(self):
        self.problem(403,self.s.send_image,self.a,self.cid,picture())
        mid=self.send();self.assertEqual(self.s.image(self.a,mid),self.s.image(self.b,mid))
        self.problem(404,self.s.image,self.c,mid);self.problem(404,self.s.send_image,self.c,self.cid,picture())
        self.assertIsNotNone(self.s.messages(self.b,self.cid)[0]['image'])
        with self.s.db() as db:
            data=db.execute('SELECT data FROM attachments').fetchone()[0];self.assertFalse(bytes(data).startswith(b'\xff\xd8'));self.assertNotIn(b'SECRET-GPS',data)
        self.s.block(self.b,self.a);self.problem(403,self.s.image,self.a,mid);self.problem(403,self.s.image,self.b,mid)
    def test_expiry_keepsake_and_removal_delete_attachment(self):
        mid=self.send();self.s.keep(self.b,mid);self.now+=14*DAY
        self.problem(404,self.s.image,self.a,mid);self.assertTrue(self.s.image(self.b,mid));self.assertIsNotNone(self.s.keepsakes(self.b)[0]['image'])
        self.s.unkeep(self.b,mid);self.problem(404,self.s.image,self.b,mid)
        with self.s.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM attachments').fetchone()[0],0)
    def test_report_evidence_outlives_deleted_account_then_expires(self):
        mid=self.send();self.s.block(self.b,self.a);self.s.report(self.b,self.a,'Test image evidence',mid)
        self.s.delete_account(self.a)
        with self.s.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM attachments').fetchone()[0],0)
            evidence=db.execute('SELECT data FROM report_attachments').fetchone()[0];self.assertTrue(self.s.cipher.decrypt(evidence))
        self.now+=90*DAY;self.s.purge()
        with self.s.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM report_attachments').fetchone()[0],0)
    def test_images_share_the_100_keepsake_limit(self):
        mid=self.send()
        for i in range(100):self.s.keep(self.b,self.s.send(self.a,self.cid,str(i))['id'])
        self.problem(409,self.s.keep,self.b,mid)
    def http(self,method,path,raw=b'',content_type='image/png',cookie='',csrf=''):
        result={};env=dict(REQUEST_METHOD=method,PATH_INFO=path,HTTP_HOST='127.0.0.1:8080',HTTP_ORIGIN='http://127.0.0.1:8080',HTTP_COOKIE=cookie,HTTP_X_CSRF_TOKEN=csrf,CONTENT_TYPE=content_type,CONTENT_LENGTH=str(len(raw)),REMOTE_ADDR='127.0.0.1');env['wsgi.input']=io.BytesIO(raw)
        body=b''.join(App(self.s)(env,lambda status,headers:result.update(status=int(status[:3]),headers=dict(headers))))
        return result,body
    def test_binary_http_upload_csrf_and_private_delivery(self):
        token,session=self.s.login('alice','A-test-password-long');cookie='am_session='+token;self.s.accept(self.b,self.cid);path=f'/api/conversations/{self.cid}/images'
        res,_=self.http('POST',path,picture(),cookie=cookie);self.assertEqual(res['status'],403)
        res,raw=self.http('POST',path,picture(),cookie=cookie,csrf=session['csrf']);self.assertEqual(res['status'],200);mid=json.loads(raw)['id']
        res,image=self.http('GET','/api/images/'+mid,cookie=cookie);self.assertEqual(res['headers']['Content-Type'],'image/jpeg');self.assertIn('no-store',res['headers']['Cache-Control']);self.assertTrue(image.startswith(b'\xff\xd8'))
        res,_=self.http('GET','/api/images/'+mid);self.assertEqual(res['status'],401)
        stranger,_=self.s.login('carol','A-test-password-long');res,_=self.http('GET','/api/images/'+mid,cookie='am_session='+stranger);self.assertEqual(res['status'],404)
        res,_=self.http('POST',path,b'<html>bad</html>',cookie=cookie,csrf=session['csrf']);self.assertEqual(res['status'],400)

if __name__=='__main__':unittest.main()
