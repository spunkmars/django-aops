#coding=utf-8

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'language/', include('account.urls.language')), #每添加一个url.py文件时，都在此加一行
    url(r'^login/$', 'account.views.common.login', name='login'),
    url(r'^logout/$', 'account.views.common.logout', name='logout'),
    url(r'^get_check_code_image/$', 'account.views.common.get_check_code_image', name='get_checkcode_image'),
    url(r'^signup/$', 'account.views.common.signup', name='signup'),
    url(r'^userprofile/(?P<user_id>\d+)/$', 'account.views.common.user_profile', name='user_profile'),
)
