"""Portable encrypted database snapshots for staging migrations and restore drills.

A distinct backup key encrypts each ordered record. No plaintext dump is written.
Restoration requires an empty destination and the original service data key.
"""
import argparse
import base64
import json
import os
from pathlib import Path
import secrets
import time
from cryptography.fernet import Fernet,InvalidToken
from .service import Service

TABLES=('districts','users','profiles','payment_events','sessions','conversations','messages','attachments','keepsakes','blocks','reports','report_attachments','rate_limits')
MAGIC=b'ANONY-MOUSES-ENCRYPTED-BACKUP-1\n'
MAX_LINE=8*1024*1024

def packed(value):
    if isinstance(value,(bytes,bytearray,memoryview)):return {'bytes':base64.b64encode(value).decode()}
    return value

def unpacked(value):
    if isinstance(value,dict):
        if set(value)!={'bytes'} or not isinstance(value['bytes'],str):raise ValueError('Invalid binary record')
        return base64.b64decode(value['bytes'],validate=True)
    if value is not None and type(value) not in (str,int,float):raise ValueError('Invalid record value')
    return value

def columns(db,kind,table):
    if kind=='sqlite':return {r['name'] for r in db.execute('PRAGMA table_info('+table+')')}
    return {r['column_name'] for r in db.execute('SELECT column_name FROM information_schema.columns WHERE table_schema=current_schema() AND table_name=?',(table,))}

def rows(db,kind,table):
    if kind=='sqlite':yield from db.execute('SELECT * FROM '+table)
    else:
        from psycopg.rows import dict_row
        with db.connection.cursor(name='backup_'+secrets.token_hex(8),row_factory=dict_row) as cur:
            cur.itersize=100;cur.execute('SELECT * FROM '+table)
            yield from cur

def snapshot(service,path,backup_key):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    # Do not create customer-data files inside publishable source directories.
    root=Path(__file__).resolve().parent.parent
    if path.resolve().is_relative_to(root) and not path.resolve().is_relative_to(root/'runtime'):
        raise ValueError('Keep backups outside source or under ignored runtime/')
    cipher=Fernet(backup_key);archive=secrets.token_hex(16);counts={t:0 for t in TABLES};seq=0
    temporary=path.with_name(path.name+'.partial-'+archive)
    def write(out,payload):
        nonlocal seq
        value={'archive':archive,'seq':seq,**payload};seq+=1
        out.write(cipher.encrypt(json.dumps(value,separators=(',',':')).encode())+b'\n')
    try:
        fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'wb') as out,service.db() as db:
            if service.database.kind=='postgres':db.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
            else:db.execute('BEGIN')
            out.write(MAGIC);write(out,{'type':'header','version':1,'tables':list(TABLES),'created':int(service.clock())})
            for table in TABLES:
                for row in rows(db,service.database.kind,table):
                    write(out,{'type':'row','table':table,'row':{k:packed(v) for k,v in dict(row).items()}});counts[table]+=1
            write(out,{'type':'footer','counts':counts});out.flush();os.fsync(out.fileno())
        # Exclusive final name prevents accidentally replacing the only known-good backup.
        os.link(temporary,path);temporary.unlink()
    except BaseException:
        temporary.unlink(missing_ok=True);raise
    return counts

def restore(service,path,backup_key):
    cipher=Fernet(backup_key);counts={t:0 for t in TABLES};seq=0;archive=None;footer=False
    def records(handle):
        while True:
            line=handle.readline(MAX_LINE+1)
            if not line:return
            if len(line)>MAX_LINE or not line.endswith(b'\n'):raise ValueError('Truncated or oversized backup record')
            try:yield json.loads(cipher.decrypt(line.strip()))
            except (InvalidToken,ValueError,UnicodeError):raise ValueError('Backup authentication failed') from None
    with open(path,'rb') as handle,service.db() as db:
        if handle.readline()!=MAGIC:raise ValueError('Not an Anony-Mouses backup')
        db.lock('restore-import')
        for table in TABLES:
            if db.execute('SELECT 1 FROM '+table+' LIMIT 1').fetchone():raise ValueError('Restore requires an empty destination')
        names={table:columns(db,service.database.kind,table) for table in TABLES}
        last_table=0
        for record in records(handle):
            if not isinstance(record,dict) or record.get('seq')!=seq or footer:raise ValueError('Invalid backup sequence')
            if seq==0:
                archive=record.get('archive')
                if record.get('type')!='header' or record.get('version')!=1 or record.get('tables')!=list(TABLES) or not isinstance(archive,str):raise ValueError('Unsupported backup header')
            elif record.get('archive')!=archive:raise ValueError('Mismatched backup archive')
            elif record.get('type')=='row':
                table=record.get('table');row=record.get('row')
                if table not in TABLES or not isinstance(row,dict) or set(row)!=names[table]:raise ValueError('Backup schema mismatch')
                index=TABLES.index(table)
                if index<last_table:raise ValueError('Backup tables are out of order')
                last_table=index;keys=list(row)
                values={k:unpacked(row[k]) for k in keys}
                encrypted_columns={'profiles':('bio','wants'),'messages':('body',),'attachments':('data',),'reports':('reason','evidence'),'report_attachments':('data',)}
                for column in encrypted_columns.get(table,()):
                    if values[column] is not None:
                        try:service.cipher.decrypt(values[column])
                        except InvalidToken:raise ValueError('Original service data key required') from None
                db.execute('INSERT INTO '+table+'('+','.join(keys)+') VALUES('+','.join('?' for _ in keys)+')',tuple(values[k] for k in keys));counts[table]+=1
            elif record.get('type')=='footer':
                if record.get('counts')!=counts:raise ValueError('Backup counts do not match')
                footer=True
            else:raise ValueError('Unsupported backup record')
            seq+=1
        if not footer:raise ValueError('Incomplete backup; restore rolled back')
        # A restored old snapshot must not make expired sessions/messages reappear.
        # Drain outside the import transaction after the complete archive authenticates.
    while True:
        deleted=service.purge(limit=500)
        if not any(deleted.values()):break
    return counts

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('operation',choices=('snapshot','restore'));parser.add_argument('path');parser.add_argument('--db',default='runtime/anony-mouse.sqlite3');args=parser.parse_args()
    data_key=os.environ.get('ANONY_MOUSE_DATA_KEY');backup_key=os.environ.get('ANONY_MOUSE_BACKUP_KEY')
    if not data_key or not backup_key:parser.error('Set ANONY_MOUSE_DATA_KEY and the separate ANONY_MOUSE_BACKUP_KEY privately')
    if data_key==backup_key:parser.error('Use a distinct backup encryption key')
    service=Service(os.environ.get('ANONY_MOUSE_DATABASE_URL') or args.db,data_key,time.time)
    try:print((snapshot if args.operation=='snapshot' else restore)(service,args.path,backup_key))
    except Exception:raise SystemExit('Backup operation failed. Destination must be empty for restore; check keys, archive and private environment configuration.') from None
    finally:service.close()
if __name__=='__main__':main()
