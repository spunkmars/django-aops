
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import cdn
 
urlpatterns = patterns('',
    url(r'^$', cdn.list_cdn, name='cdn_index'),
    url(r'add/$', cdn.add_cdn, name='add_cdn'),
    url(r'del/(?P<cdn_id>\d+)/$', cdn.del_cdn, name='del_cdn'),
    url(r'(?P<cdn_id>\d+)/$', cdn.edit_cdn, name='edit_cdn'),
    url(r'list/$', cdn.list_cdn, name='list_cdn'),
)

