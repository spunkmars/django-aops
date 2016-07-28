
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import domain_name
 
urlpatterns = patterns('',
    url(r'^$', domain_name.list_domain_name, name='domain_name_index'),
    url(r'add/$', domain_name.add_domain_name, name='add_domain_name'),
    url(r'del/(?P<domain_name_id>\d+)/$', domain_name.del_domain_name, name='del_domain_name'),
    url(r'(?P<domain_name_id>\d+)/$', domain_name.edit_domain_name, name='edit_domain_name'),
    url(r'list/$', domain_name.list_domain_name, name='list_domain_name'),
)

