
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import ip_record
 
urlpatterns = patterns('',
    url(r'^$', ip_record.list_ip_record, name='ip_record_index'),
    url(r'add/$', ip_record.add_ip_record, name='add_ip_record'),
    url(r'del/(?P<ip_record_id>\d+)/$', ip_record.del_ip_record, name='del_ip_record'),
    url(r'(?P<ip_record_id>\d+)/$', ip_record.edit_ip_record, name='edit_ip_record'),
    url(r'list/$', ip_record.list_ip_record, name='list_ip_record'),
)

