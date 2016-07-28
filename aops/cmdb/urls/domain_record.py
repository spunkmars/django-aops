
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import domain_record
 
urlpatterns = patterns('',
    url(r'^$', domain_record.list_domain_record, name='domain_record_index'),
    url(r'add/$', domain_record.add_domain_record, name='add_domain_record'),
    url(r'del/(?P<domain_record_id>\d+)/$', domain_record.del_domain_record, name='del_domain_record'),
    url(r'(?P<domain_record_id>\d+)/$', domain_record.edit_domain_record, name='edit_domain_record'),
    url(r'list/$', domain_record.list_domain_record, name='list_domain_record'),
)

