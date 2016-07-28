
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import ip_resource
 
urlpatterns = patterns('',
    url(r'^$', ip_resource.list_ip_resource, name='ip_resource_index'),
    url(r'add/$', ip_resource.add_ip_resource, name='add_ip_resource'),
    url(r'del/(?P<ip_resource_id>\d+)/$', ip_resource.del_ip_resource, name='del_ip_resource'),
    url(r'(?P<ip_resource_id>\d+)/$', ip_resource.edit_ip_resource, name='edit_ip_resource'),
    url(r'list/$', ip_resource.list_ip_resource, name='list_ip_resource'),
)

