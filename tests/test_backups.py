import io
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from cryptography.fernet import Fernet
from backend.service import Service,Problem,DAY
from backend.backups import snapshot,restore
from backend.districts import bundled_districts
from support import service_for_test

class BackupTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.now=1791980000;self.key=Fernet.generate_key();self.backup_key=Fernet.generate_key()
        self.source=Service(Path(self.tmp.name)/'source',self.key,lambda:self.now);self.addCleanup(self.source.close)
        self.source.seed_districts([('GU2',51.24,-.59)])
        self.users=[]
        for name in ('alice','bob'):
            uid=self.source.register(dict(login=name,password='A-test-password-long',alias=name,bio='PRIVATE-DESCRIPTION',wants='Test hello',district='GU2',age_range='40s',adult=True,consent=True))['user_id']
            self.source.record_month_payment(uid,'development',name,2000,'GBP',offer_code='website');self.users.append(uid)
        self.cid=self.source.request(*self.users)['id'];self.source.accept(self.users[1],self.cid)
        self.mid=self.source.send(self.users[0],self.cid,'PRIVATE-MESSAGE')['id'];self.source.keep(self.users[1],self.mid)
        image=io.BytesIO();Image.new('RGB',(20,20),'blue').save(image,'PNG')
        self.image=self.source.send_image(self.users[0],self.cid,image.getvalue())['id']
        self.token,_=self.source.login('alice','A-test-password-long',True)
        self.path=Path(self.tmp.name)/'encrypted.backup'
    def target(self,key=None):return service_for_test(self,Path(self.tmp.name)/('target-'+str(len(list(Path(self.tmp.name).iterdir())))),key or self.key,lambda:self.now)
    def test_encrypted_portable_restore_preserves_access_and_private_images(self):
        counts=snapshot(self.source,self.path,self.backup_key);data=self.path.read_bytes()
        for secret in (b'PRIVATE-DESCRIPTION',b'PRIVATE-MESSAGE',b'alice',self.token.encode()):self.assertNotIn(secret,data)
        self.assertEqual(self.path.stat().st_mode&0o777,0o600)
        target=self.target();self.assertEqual(restore(target,self.path,self.backup_key),counts)
        self.assertEqual(target.profile(self.users[0])['bio'],'PRIVATE-DESCRIPTION')
        self.assertTrue(target.membership(self.users[0])['active'])
        self.assertEqual(target.authenticate(self.token),self.users[0])
        self.assertEqual(target.image(self.users[1],self.image),self.source.image(self.users[1],self.image))
        self.assertIn(self.mid,[m['id'] for m in target.keepsakes(self.users[1])])
        second=Path(self.tmp.name)/'second.backup';snapshot(target,second,self.backup_key)
        replay=self.target();restore(replay,second,self.backup_key)
        self.assertEqual(replay.image(self.users[1],self.image),target.image(self.users[1],self.image))
    def test_corrupt_or_truncated_archive_rolls_back_every_record(self):
        snapshot(self.source,self.path,self.backup_key)
        lines=self.path.read_bytes().splitlines(keepends=True);self.path.write_bytes(b''.join(lines[:-1]))
        target=self.target()
        with self.assertRaises(ValueError):restore(target,self.path,self.backup_key)
        with target.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM users').fetchone()[0],0)
    def test_wrong_backup_or_data_key_and_nonempty_destination_are_rejected(self):
        snapshot(self.source,self.path,self.backup_key)
        with self.assertRaises(ValueError):restore(self.target(),self.path,Fernet.generate_key())
        target=self.target(Fernet.generate_key())
        with self.assertRaises(ValueError):restore(target,self.path,self.backup_key)
        with target.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM users').fetchone()[0],0)
        with self.assertRaises(ValueError):restore(self.source,self.path,self.backup_key)
        with self.assertRaises(FileExistsError):snapshot(self.source,self.path,self.backup_key)
    def test_restore_reapplies_expiry_without_destroying_saved_copy(self):
        snapshot(self.source,self.path,self.backup_key);self.now+=31*DAY
        target=self.target();restore(target,self.path,self.backup_key)
        with self.assertRaises(Problem):target.authenticate(self.token)
        self.assertFalse(target.membership(self.users[0])['active'])
        self.assertEqual(target.messages(self.users[0],self.cid),[])
        self.assertEqual([m['id'] for m in target.messages(self.users[1],self.cid)],[self.mid])
        with target.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM attachments').fetchone()[0],0)
    def test_archive_reordering_is_detected(self):
        snapshot(self.source,self.path,self.backup_key)
        lines=self.path.read_bytes().splitlines(keepends=True);lines[2],lines[3]=lines[3],lines[2];self.path.write_bytes(b''.join(lines))
        with self.assertRaises(ValueError):restore(self.target(),self.path,self.backup_key)
    def test_nationwide_district_import_is_approximate_and_idempotent(self):
        districts=bundled_districts();self.assertGreater(len(districts),2900)
        self.source.seed_districts(districts);self.source.seed_districts(districts)
        with self.source.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM districts').fetchone()[0],len(districts))
            self.assertIsNotNone(db.execute("SELECT code FROM districts WHERE code='M1'").fetchone())
            self.assertIsNotNone(db.execute("SELECT code FROM districts WHERE code='ZE1'").fetchone())

if __name__=='__main__':unittest.main()
