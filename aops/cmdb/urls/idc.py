
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import idc
 
urlpatterns = patterns('',
    url(r'^$', idc.list_idc, name='idc_index'),
    url(r'add/$', idc.add_idc, name='add_idc'),
    url(r'del/(?P<idc_id>\d+)/$', idc.del_idc, name='del_idc'),
    url(r'(?P<idc_id>\d+)/$', idc.edit_idc, name='edit_idc'),
    url(r'list/$', idc.list_idc, name='list_idc'),
)

