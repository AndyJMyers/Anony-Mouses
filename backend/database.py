"""Versioned SQLite development / pooled PostgreSQL storage.

SQL parameters remain bound; the qmark adapter is for our fixed SQL only.
Never log connection strings. PostgreSQL still runs the fictional service only.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
import hashlib
import json
import math
import sqlite3

MIGRATIONS=Path(__file__).with_name('migrations')
IntegrityError=sqlite3.IntegrityError

def kilometres(a,b,c,d):
    a,b,c,d=map(math.radians,(a,b,c,d))
    v=math.sin((c-a)/2)**2+math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    return 6371*2*math.asin(min(1,math.sqrt(max(0,v))))

class Row(dict):
    def __getitem__(self,key):
        return tuple(self.values())[key] if isinstance(key,int) else super().__getitem__(key)

class Cursor:
    def __init__(self,cursor):self.cursor=cursor
    @property
    def rowcount(self):return self.cursor.rowcount
    def fetchone(self):
        r=self.cursor.fetchone();return Row(r) if r is not None else None
    def fetchall(self):return [Row(r) for r in self.cursor.fetchall()]
    def __iter__(self):
        for r in self.cursor:yield Row(r)

class Transaction:
    def __init__(self,connection,kind):self.connection,self.kind=connection,kind
    def execute(self,sql,parameters=()):
        if self.kind=='sqlite':return self.connection.execute(sql,parameters)
        # Only application-controlled SQL is accepted here. No SQL contains a literal '?'.
        try:return Cursor(self.connection.execute(sql.replace('?','%s'),parameters))
        except Exception as exc:
            import psycopg
            if isinstance(exc,psycopg.IntegrityError):raise IntegrityError('Database constraint rejected the operation') from exc
            raise
    def executescript(self,sql):
        if self.kind=='sqlite':return self.connection.executescript(sql)
        self.connection.execute(sql)
    def lock(self,key):
        if self.kind=='sqlite':
            if not self.connection.in_transaction:self.connection.execute('BEGIN IMMEDIATE')
        else:
            number=int.from_bytes(hashlib.sha256(key.encode()).digest()[:8],signed=True)
            self.connection.execute('SELECT pg_advisory_xact_lock(%s)',(number,))

class Database:
    def __init__(self,target,*,pool_size=8):
        self.kind='postgres' if str(target).startswith(('postgres://','postgresql://','host=','dbname=')) or 'dbname=' in str(target) else 'sqlite'
        self.target=str(target);self.current=ContextVar('anony_transaction_'+str(id(self)),default=None)
        self.pool=None
        if self.kind=='postgres':
            from psycopg.rows import dict_row
            from psycopg_pool import ConnectionPool
            self.pool=ConnectionPool(self.target,min_size=1,max_size=pool_size,timeout=10,max_waiting=32,
                kwargs={'row_factory':dict_row,'connect_timeout':5},configure=self._configure,open=False)
            self.pool.open(wait=True,timeout=10)
        else:Path(self.target).parent.mkdir(parents=True,exist_ok=True)
        self.migrate()
    @staticmethod
    def _configure(conn):
        conn.execute('SET statement_timeout=10000');conn.execute('SET lock_timeout=5000');conn.commit()
    @contextmanager
    def connection(self):
        existing=self.current.get()
        if existing is not None:
            yield existing;return
        if self.kind=='postgres':
            with self.pool.connection() as conn:
                tx=Transaction(conn,self.kind);token=self.current.set(tx)
                try:yield tx
                finally:self.current.reset(token)
        else:
            conn=sqlite3.connect(self.target,timeout=10);conn.row_factory=sqlite3.Row
            conn.execute('PRAGMA foreign_keys=ON');conn.execute('PRAGMA secure_delete=ON')
            conn.create_function('am_distance',4,kilometres,deterministic=True)
            conn.create_function('floor',1,math.floor,deterministic=True)
            token=self.current.set(Transaction(conn,self.kind))
            try:
                with conn:yield self.current.get()
            finally:self.current.reset(token);conn.close()
    def migrate(self):
        with self.connection() as db:
            db.lock('schema-migrations')
            db.execute('CREATE TABLE IF NOT EXISTS schema_migrations(version INTEGER PRIMARY KEY)')
            versions={r['version'] for r in db.execute('SELECT version FROM schema_migrations')}
            if 1 not in versions:
                # SQLite executescript would commit the migration lock, so use individual DDL statements.
                sql=(MIGRATIONS/f'001_{self.kind}.sql').read_text()
                for statement in sql.split(';'):
                    if statement.strip():db.execute(statement)
                db.execute('INSERT INTO schema_migrations VALUES(?)',(1,))
            if self.kind=='sqlite':
                # Recheck additive legacy columns: old development fixtures can lack these.
                for table,columns in {'profiles':{'avatar':"TEXT NOT NULL DEFAULT '{}'"},'payment_events':{'starts_at':'INTEGER NOT NULL DEFAULT 0','offer_code':"TEXT NOT NULL DEFAULT 'launch'",'requested_start':'INTEGER','voucher_code':"TEXT NOT NULL DEFAULT ''"}}.items():
                    present={r['name'] for r in db.execute('PRAGMA table_info('+table+')')}
                    for column,definition in columns.items():
                        if column not in present:db.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')
                db.execute("CREATE UNIQUE INDEX IF NOT EXISTS voucher_once ON payment_events(user_id,voucher_code) WHERE voucher_code != ''")
                db.execute('CREATE INDEX IF NOT EXISTS payment_access ON payment_events(user_id,starts_at,access_until)')
            if 2 not in versions:
                for row in db.execute('SELECT user_id,avatar FROM profiles').fetchall():
                    avatar=json.loads(row['avatar'])
                    if 'build' in avatar or 'chest' in avatar:
                        avatar.pop('build',None);avatar.pop('chest',None)
                        db.execute('UPDATE profiles SET avatar=? WHERE user_id=?',(json.dumps(avatar),row['user_id']))
                db.execute('INSERT INTO schema_migrations VALUES(?)',(2,))
            # Idempotent indexes also repair legacy fixtures reconstructed in development tests.
            for statement in (MIGRATIONS/'003_indexes.sql').read_text().split(';'):
                if statement.strip():db.execute(statement)
            if 3 not in versions:db.execute('INSERT INTO schema_migrations VALUES(?)',(3,))
            if self.kind=='postgres' and 4 not in versions:
                db.executescript((MIGRATIONS/'004_postgres_distance.sql').read_text())
                db.execute('INSERT INTO schema_migrations VALUES(?)',(4,))
            if 5 not in versions:
                for statement in (MIGRATIONS/'005_rate_limits.sql').read_text().split(';'):
                    if statement.strip():db.execute(statement)
                db.execute('INSERT INTO schema_migrations VALUES(?)',(5,))
    def close(self):
        if self.pool:self.pool.close()
