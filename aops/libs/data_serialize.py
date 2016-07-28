#-*- coding: utf-8 -*-

import sys

if  sys.version_info >= (2, 6, 0):
    import json as json
else:
    import simplejson as json

from common import Common

class DataSerialize(Common):

    def __init__(self, *args, **kwargs):
        format = kwargs.get('format', 'json')
        if 'format' in kwargs:
            del kwargs['format']
        self.kwargs = kwargs
        if format == 'json':
            self.serialize = self.data_to_json
            self.deserialize = self.json_to_data

        if format == 'xml':
            self.serialize = self.data_to_xml
            self.deserialize = self.xml_to_data


    def data_to_json(self, json_d=None, **kwargs):
        akwargs = dict(self.kwargs, **kwargs)
        #self.DD(akwargs)
        json_str = json.dumps(json_d,  **akwargs)
        return json_str


    def json_to_data(self, json_str='', **kwargs):
        akwargs = dict(self.kwargs, **kwargs)
        #self.DD(akwargs)
        json_d = json.loads(json_str,  **akwargs)
        return json_d


    def data_to_xml(self):
        pass


    def xml_to_data(self):
        pass


#    def serialize(self, *args, **kwargs):
#        return self.data_to_json(*args, **kwargs)


#    def deserialize(self, *args, **kwargs):
#        return self.json_to_data(*args, **kwargs)