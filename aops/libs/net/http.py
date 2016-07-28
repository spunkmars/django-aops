# -*- coding: utf-8 -*-

import sys
import copy
import os
import httplib, urllib
from urlparse import urlparse

from libs.common import Common
from libs.data_serialize import DataSerialize

class Http(Common):

    def __init__(self, *args, **kwargs):
        self.data_format = kwargs.get('data_format', 'json')
        self.ds = DataSerialize(format=self.data_format)
        error_info = {'error_reason':'', 'error_code':0}
        self.error_info = kwargs.get('error_info', error_info)
        self.is_data_serialize = kwargs.get('is_data_serialize', 0)
        if kwargs.has_key('is_data_serialize'):
            self.is_data_serialize = kwargs.get('is_data_serialize', 0)
            self.is_send_data_serialize = self.is_data_serialize
            self.is_rec_data_deserialize = self.is_data_serialize
        else:
            self.is_send_data_serialize = kwargs.get('is_send_data_serialize', 0)
            self.is_rec_data_deserialize = kwargs.get('is_rec_data_deserialize', 0)
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        self.headers = kwargs.get('headers', headers)


    def reset_error_info(self):
        self.error_info = {'error_reason':'', 'error_code':0}


    def set_http_headers(self, headers={}):
        self.headers = headers


    def update_http_headers(self, headers={}):
        self.headers.update(headers)


    def parse_uri(self, uri=None):
        if sys.version_info >= (2, 5, 0):
            url_h = urlparse(uri)
            url_scheme = url_h.scheme
            url_hostname = url_h.hostname
            url_port = url_h.port
            url_path = url_h.path
        else:
            url_h = urlparse(uri)
            url_scheme = url_h[0]
            host_a = url_h[1].split(':')
            url_hostname = host_a[0]
            if  len(host_a) == 2:
                url_port = host_a[1]
            else:
                url_port = None
            url_path = url_h[2]

        uri_h = {'scheme':url_scheme, 'hostname':url_hostname, 'port':url_port, 'path':url_path}
        return uri_h


    def http_connect(self, content={}, api_url=None ,http_method='POST'):
        self.error_code = 0
        self.error_reason = ''

        self.reset_error_info()
        uri_h = self.parse_uri(uri=api_url)
        api_url_scheme = uri_h['scheme']
        api_url_hostname = uri_h['hostname']
        api_url_port = uri_h['port']
        api_url_path = uri_h['path']
        data = None
        error = None
        if api_url_scheme == 'https':
            conn = httplib.HTTPSConnection(api_url_hostname, api_url_port)
        elif api_url_scheme == 'http' :
            conn = httplib.HTTPConnection(api_url_hostname, api_url_port)
        else :
              self.error_code = 1
              self.error_reason = 'invalid url !'
        # print 'method: %s,   url:%s' % (http_method,  api_url_path)
        # self.DD(content)
        # self.DD(self.headers)
        conn.request(http_method,  api_url_path , content, self.headers)
        response = conn.getresponse()

        if response.status in (301, 302, 304, 307) :
            print response.getheader("Location")
            exit

        # print 'stats:%s, reason:%s' % (response.status, response.reason)
        if  response.status in (200, 202) and response.reason in ( 'OK', 'Accepted') :
            data = response.read()
            conn.close()
            return data
        else :
            if response.status == 401:
                self.error_info['error_code'] = 2
            else:
                self.error_info['error_code'] = 1
            self.error_info['error_reason'] = 'connect %s error: status>%s  reason> %s' % (api_url, response.status, response.reason )
        conn.close()


    def api_connect(self, params={}, api_url=None, http_method='POST' ):
        self.error_code = 0
        self.error_reason = ''
        self.reset_error_info()
        data = None
        error = None
        if self.is_send_data_serialize == 1:
            params = self.ds.serialize( params )
        else:
            params = urllib.urlencode(params)
        data = self.http_connect(content=params, api_url=api_url, http_method=http_method)
        # self.DD(data)
        # self.DD(self.error_info)
        if self.error_info['error_code'] == 0 and self.is_rec_data_deserialize == 1:
            data = self.ds.deserialize( data )
        return data