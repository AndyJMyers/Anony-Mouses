"""Run the same service tests on SQLite or isolated PostgreSQL schemas."""
import os
import uuid
from backend.service import Service

def service_for_test(owner,path,key,clock):
    url=os.environ.get('ANONY_TEST_DATABASE_URL')
    if not url:return Service(path,key,clock)
    import psycopg
    from psycopg import sql
    from psycopg.conninfo import make_conninfo
    schema='test_'+uuid.uuid4().hex
    with psycopg.connect(url,autocommit=True) as conn:conn.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
    def drop_schema():
        with psycopg.connect(url,autocommit=True) as conn:conn.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(schema)))
    owner.addCleanup(drop_schema)
    service=Service(make_conninfo(url,options='-c search_path='+schema),key,clock)
    owner.addCleanup(service.close)
    return service
