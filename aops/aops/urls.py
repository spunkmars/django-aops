from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import cmdb

urlpatterns = patterns('',
    url(r'^$', lambda x: HttpResponseRedirect(reverse('dashboard'))),
    url(r'^index/$', 'cmdb.views.dashboard.dashboard', name='site_index'),
    url(r'^dashboard/$', 'cmdb.views.dashboard.dashboard', name='dashboard'),
    url(r'^dashboard_ajax/$', 'cmdb.views.dashboard.dashboard_ajax', name='dashboard_ajax'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^cmdb/', include('cmdb.urls', namespace='cmdb', app_name='cmdb')),
    url(r'^accounts/', include('account.urls', namespace='account', app_name='account')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('haystack.urls')),
    url(r'^export/', include('export.urls', namespace='export', app_name='export')),
)
