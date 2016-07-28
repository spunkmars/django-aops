
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import contract
 
urlpatterns = patterns('',
    url(r'^$', contract.list_contract, name='contract_index'),
    url(r'add/$', contract.add_contract, name='add_contract'),
    url(r'del/(?P<contract_id>\d+)/$', contract.del_contract, name='del_contract'),
    url(r'(?P<contract_id>\d+)/$', contract.edit_contract, name='edit_contract'),
    url(r'list/$', contract.list_contract, name='list_contract'),
)

