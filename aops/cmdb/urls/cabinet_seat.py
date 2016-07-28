
#coding=utf-8

from django.conf.urls import patterns, url, include

from cmdb.views import cabinet_seat
 
urlpatterns = patterns('',
    url(r'^$', cabinet_seat.list_cabinet_seat, name='cabinet_seat_index'),
    url(r'add/$', cabinet_seat.add_cabinet_seat, name='add_cabinet_seat'),
    url(r'del/(?P<cabinet_seat_id>\d+)/$', cabinet_seat.del_cabinet_seat, name='del_cabinet_seat'),
    url(r'(?P<cabinet_seat_id>\d+)/$', cabinet_seat.edit_cabinet_seat, name='edit_cabinet_seat'),
    url(r'list/$', cabinet_seat.list_cabinet_seat, name='list_cabinet_seat'),
)

