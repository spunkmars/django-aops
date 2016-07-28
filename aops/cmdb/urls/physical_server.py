
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import physical_server
 
urlpatterns = patterns('',
    url(r'^$', physical_server.list_physical_server, name='physical_server_index'),
    url(r'add/$', physical_server.add_physical_server, name='add_physical_server'),
    url(r'del/(?P<physical_server_id>\d+)/$', physical_server.del_physical_server, name='del_physical_server'),
    url(r'(?P<physical_server_id>\d+)/$', physical_server.edit_physical_server, name='edit_physical_server'),
    url(r'list/$', physical_server.list_physical_server, name='list_physical_server'),
)

