#coding=utf-8
from django.conf.urls import patterns, url, include
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from cmdb.views import deal_import_data
from cmdb.views import get_ip_rel_info

urlpatterns = patterns('',
    url(r'^$', lambda x: HttpResponseRedirect(reverse('cmdb:list_host'))),

    url(r'idc/', include('cmdb.urls.idc')),

    url(r'cdn_domain_record/', include('cmdb.urls.cdn_domain_record')),

    url(r'idc_contract/', include('cmdb.urls.idc_contract')),

    url(r'contract/', include('cmdb.urls.contract')),

    url(r'contacts/', include('cmdb.urls.contacts')),

    url(r'device/', include('cmdb.urls.device')),

    url(r'domain_name/', include('cmdb.urls.domain_name')),

    url(r'cdn/', include('cmdb.urls.cdn')),

    url(r'ip_resource/', include('cmdb.urls.ip_resource')),

    url(r'ip_record/', include('cmdb.urls.ip_record')),

    url(r'cabinet/', include('cmdb.urls.cabinet')),

    url(r'cabinet_seat/', include('cmdb.urls.cabinet_seat')),

    url(r'physical_server/', include('cmdb.urls.physical_server')),

    url(r'host/', include('cmdb.urls.host')),

    url(r'network_equipment/', include('cmdb.urls.network_equipment')),

    url(r'domain_record/', include('cmdb.urls.domain_record')),

    url(r'company/', include('cmdb.urls.company')),

    url(r'brand/', include('cmdb.urls.brand')),

)
