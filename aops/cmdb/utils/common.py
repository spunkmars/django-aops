#coding=utf-8

from hashlib import md5
import time

def create_uuid(*args):
    id = md5()
    timestamp=time.time()
    id.update('%s%f'% (''.join(args).encode('utf8') ,timestamp))
    id = id.hexdigest()[8:-8].upper()
    return id