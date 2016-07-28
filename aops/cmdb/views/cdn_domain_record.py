#coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q

from libs.views.common import list_data, del_model_items, display_confirm_msg

from cmdb.models.cdn_domain_record import CdnDomainRecord
from cmdb.forms.cdn_domain_record import CdnDomainRecordForm
from django.views.decorators.csrf import csrf_exempt
import json
from libs.models.common import del_model_data

def app_info():
    app = {
      "name" : "cmdb",
      "fun"  : "cdn_domain_record",
      "edit_url" : 'cmdb:edit_cdn_domain_record',
      "del_url" : 'cmdb:del_cdn_domain_record'
    }
    return app

@csrf_exempt #禁用csrf
def add_cdn_domain_record(request):
    if request.method == 'POST':
        form = CdnDomainRecordForm(model=CdnDomainRecord, data=request.POST)
        if form.is_valid():
            new_cdn_domain_record = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_cdn_domain_record'))
    else:
        form = CdnDomainRecordForm(model=CdnDomainRecord)
    app = app_info()
    app['location'] = 'add'
    return render_to_response('add_data.html', {'form': form, 'app':app} ,context_instance=RequestContext(request))


@csrf_exempt #禁用csrf
def edit_cdn_domain_record(request, cdn_domain_record_id):
    idc_contract = get_object_or_404(CdnDomainRecord, pk=cdn_domain_record_id)
    if request.method == 'POST':
        form = CdnDomainRecordForm(model=CdnDomainRecord, instance=idc_contract, data=request.POST)
        if form.is_valid():
           new_cdn_domain_record = form.save()
           return HttpResponseRedirect(reverse('cmdb:list_cdn_domain_record'))
    else:
        form = CdnDomainRecordForm(model=CdnDomainRecord, instance=idc_contract)

    app = app_info()
    app['location'] = 'edit'
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app} ,context_instance=RequestContext(request))

@csrf_exempt #禁用csrf
def list_cdn_domain_record(request):
    model_object = CdnDomainRecord
    template_file = 'list_data.html'
    show_field_list = [ 'cdn',
                        'domain_record']
    filter_field = 'id'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'

    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_cdn_domain_record(request, cdn_domain_record_id):
    del_res={}
    if request.method == "POST":
        del_res = del_model_data(model=CdnDomainRecord, id=cdn_domain_record_id)

    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")


