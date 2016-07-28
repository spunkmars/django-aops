
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import brand
 
urlpatterns = patterns('',
    url(r'^$', brand.list_brand, name='brand_index'),
    url(r'add/$', brand.add_brand, name='add_brand'),
    url(r'del/(?P<brand_id>\d+)/$', brand.del_brand, name='del_brand'),
    url(r'(?P<brand_id>\d+)/$', brand.edit_brand, name='edit_brand'),
    url(r'list/$', brand.list_brand, name='list_brand'),
)

