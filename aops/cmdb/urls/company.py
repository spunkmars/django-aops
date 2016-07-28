
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import company
 
urlpatterns = patterns('',
    url(r'^$', company.list_company, name='company_index'),
    url(r'add/$', company.add_company, name='add_company'),
    url(r'del/(?P<company_id>\d+)/$', company.del_company, name='del_company'),
    url(r'(?P<company_id>\d+)/$', company.edit_company, name='edit_company'),
    url(r'list/$', company.list_company, name='list_company'),
)

