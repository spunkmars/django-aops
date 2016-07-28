
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import device
 
urlpatterns = patterns('',
    url(r'^$', device.list_device, name='device_index'),
    url(r'add/$', device.add_device, name='add_device'),
    url(r'del/(?P<device_id>\d+)/$', device.del_device, name='del_device'),
    url(r'(?P<device_id>\d+)/$', device.edit_device, name='edit_device'),
    url(r'list/$', device.list_device, name='list_device'),
)

