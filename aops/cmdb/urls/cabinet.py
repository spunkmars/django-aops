
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import cabinet
 
urlpatterns = patterns('',
    url(r'^$', cabinet.list_cabinet, name='cabinet_index'),
    url(r'add/$', cabinet.add_cabinet, name='add_cabinet'),
    url(r'del/(?P<cabinet_id>\d+)/$', cabinet.del_cabinet, name='del_cabinet'),
    url(r'(?P<cabinet_id>\d+)/$', cabinet.edit_cabinet, name='edit_cabinet'),
    url(r'list/$', cabinet.list_cabinet, name='list_cabinet'),
)

