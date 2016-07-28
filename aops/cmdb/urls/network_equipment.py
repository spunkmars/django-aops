
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import network_equipment
 
urlpatterns = patterns('',
    url(r'^$', network_equipment.list_network_equipment, name='network_equipment_index'),
    url(r'add/$', network_equipment.add_network_equipment, name='add_network_equipment'),
    url(r'del/(?P<network_equipment_id>\d+)/$', network_equipment.del_network_equipment, name='del_network_equipment'),
    url(r'(?P<network_equipment_id>\d+)/$', network_equipment.edit_network_equipment, name='edit_network_equipment'),
    url(r'list/$', network_equipment.list_network_equipment, name='list_network_equipment'),
)

