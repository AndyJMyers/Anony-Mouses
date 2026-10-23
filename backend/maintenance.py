"""Bounded expiry worker for fictional staging data; no production evidence policy."""
import argparse
from contextlib import contextmanager
import os
import threading
import time
from .service import Service

@contextmanager
def cleaner(service,interval=60,batch_size=500):
    stop=threading.Event()
    def work():
        while not stop.is_set():
            try:service.purge(limit=batch_size)
            except Exception:print('Expiry batch failed; the next interval will retry.',flush=True)
            stop.wait(interval)
    thread=threading.Thread(target=work,name='anony-expiry',daemon=True);thread.start()
    try:yield
    finally:stop.set();thread.join(timeout=12)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',default='runtime/anony-mouse.sqlite3');p.add_argument('--batch-size',type=int,default=500);p.add_argument('--interval',type=int,default=60);p.add_argument('--once',action='store_true');args=p.parse_args()
    if not 1<=args.batch_size<=5000 or not 1<=args.interval<=60:p.error('Batch must be 1–5000 and interval 1–60 seconds')
    key=os.environ.get('ANONY_MOUSE_DATA_KEY')
    if not key:p.error('Set ANONY_MOUSE_DATA_KEY privately in the environment')
    s=Service(os.environ.get('ANONY_MOUSE_DATABASE_URL') or args.db,key,time.time)
    try:
        if args.once:print(s.purge(limit=args.batch_size));return
        stop=threading.Event()
        import signal
        for signum in (signal.SIGTERM,signal.SIGINT):signal.signal(signum,lambda *_:stop.set())
        while not stop.is_set():
            print(s.purge(limit=args.batch_size),flush=True);stop.wait(args.interval)
    finally:s.close()
if __name__=='__main__':main()
