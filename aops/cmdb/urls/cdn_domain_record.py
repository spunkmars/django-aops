
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import cdn_domain_record
 
urlpatterns = patterns('',
    url(r'^$', cdn_domain_record.list_cdn_domain_record, name='cdn_domain_record_index'),
    url(r'add/$', cdn_domain_record.add_cdn_domain_record, name='add_cdn_domain_record'),
    url(r'del/(?P<cdn_domain_record_id>\d+)/$', cdn_domain_record.del_cdn_domain_record, name='del_cdn_domain_record'),
    url(r'(?P<cdn_domain_record_id>\d+)/$', cdn_domain_record.edit_cdn_domain_record, name='edit_cdn_domain_record'),
    url(r'list/$', cdn_domain_record.list_cdn_domain_record, name='list_cdn_domain_record'),
)

