#coding=utf-8

import uuid
import pprint
from datetime import datetime

class Common(object):

    def __init__(self):
        pass


    def DD(self, vars):
        pprint.pprint(vars)


    def get_uuid(self):
        uuid_1 = uuid.uuid1()
        uuid_4 = uuid.uuid4()
        return '%s-%s' % (uuid_1, uuid_4)


    def get_create_date(self):
        return datetime.now().strftime('%Y%m%d%H%M%S')


def trans_encode(input='', c_type='utf-8'):
    if type(input) == unicode:
        input =  input.encode(c_type)
        return input
    else:
        return input