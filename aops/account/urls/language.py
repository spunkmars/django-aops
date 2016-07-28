#coding=utf-8
from django.conf.urls import patterns, url, include

from account.views import language

urlpatterns = patterns('',
    url(r'^$', language.list_language, name='all_lang'),
    url(r'list/$', language.list_language, name='list_lang'),
    url(r'select/$', language.select_language, name='select_lang'),
)
