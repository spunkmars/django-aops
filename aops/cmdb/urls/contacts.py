
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import contacts
 
urlpatterns = patterns('',
    url(r'^$', contacts.list_contacts, name='contacts_index'),
    url(r'add/$', contacts.add_contacts, name='add_contacts'),
    url(r'del/(?P<contacts_id>\d+)/$', contacts.del_contacts, name='del_contacts'),
    url(r'(?P<contacts_id>\d+)/$', contacts.edit_contacts, name='edit_contacts'),
    url(r'list/$', contacts.list_contacts, name='list_contacts'),
)

