#coding=utf-8
import re

__author__ = 'SA'


def transString(v):
    return '%s' % v


class salt(object):
    def __init__(self, **kw):
        self.id = kw.get('id', 0)
        self.rule =kw.get('rule', '')
        self.info = kw.get('info', '')
        self.sp_key = kw.get('sp_key', '')

    def create(self, *args):
        from hashlib import md5
        self.id = md5()
        args = map(transString,args)
        self.id.update("".join(args))
        self.id = self.id.hexdigest()[8:-8].upper()
        return self.id

    def filter(self,rule = '',info = ''):
        '''
        >>> config={'rule':'\d', 'info':'12'}
        >>> k=salt(**config)
        >>> print k.filter()
        ['1', '2']
        >>> print k.filter(1, '123')
        ['1']
        >>> print k.filter(1, 'abc')
        []
        '''
        self.r_con = str(rule) if rule else self.rule
        self.i_con = str(info) if info else self.info
        r=re.compile(self.r_con)
        return r.findall(self.i_con)



if __name__ == '__main__':
    import doctest
    doctest.testmod()

