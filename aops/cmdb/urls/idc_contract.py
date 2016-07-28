
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import idc_contract
 
urlpatterns = patterns('',
    url(r'^$', idc_contract.list_idc_contract, name='idc_contract_index'),
    url(r'add/$', idc_contract.add_idc_contract, name='add_idc_contract'),
    url(r'del/(?P<idc_contract_id>\d+)/$', idc_contract.del_idc_contract, name='del_idc_contract'),
    url(r'(?P<idc_contract_id>\d+)/$', idc_contract.edit_idc_contract, name='edit_idc_contract'),
    url(r'list/$', idc_contract.list_idc_contract, name='list_idc_contract'),
)

