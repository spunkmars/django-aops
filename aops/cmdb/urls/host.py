
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import host
 
urlpatterns = patterns('',
    url(r'^$', host.list_host, name='host_index'),
    url(r'add/$', host.add_host, name='add_host'),
    url(r'del/(?P<host_id>\d+)/$', host.del_host, name='del_host'),
    url(r'(?P<host_id>\d+)/$', host.edit_host, name='edit_host'),
    url(r'get_salt_id/$', host.get_salt_id, name='get_salt_id'),
    url(r'get_uuid/$', host.get_uuid, name='get_uuid'),
    url(r'list/$', host.list_host, name='list_host'),
)

