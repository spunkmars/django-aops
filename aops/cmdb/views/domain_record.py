#coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q

from libs.views.common import list_data, del_model_items, display_confirm_msg

from cmdb.models.domain_record import DomainRecord
from cmdb.forms.domain_record import DomainRecordForm
from django.views.decorators.csrf import csrf_exempt
import json
from libs.models.common import del_model_data

def app_info():
    app = {
      "name" : "cmdb",
      "fun"  : "domain_record",
      "edit_url" : 'cmdb:edit_domain_record',
      "del_url" : 'cmdb:del_domain_record'
    }
    return app

@csrf_exempt #禁用csrf
def add_domain_record(request):
    if request.method == 'POST':
        form = DomainRecordForm(model=DomainRecord, data=request.POST)
        if form.is_valid():
            new_domain_record = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_domain_record'))
    else:
        form = DomainRecordForm(model=DomainRecord)
    app = app_info()
    app['location'] = 'add'
    m2m_fs = DomainRecord._meta.many_to_many
    m2m_list=[]
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    return render_to_response('add_data.html',
                                  { 'form': form, 'app':app, 'm2m_list':m2m_list} ,context_instance=RequestContext(request))


@csrf_exempt #禁用csrf
def edit_domain_record(request, domain_record_id):
    domain_record = get_object_or_404(DomainRecord, pk=domain_record_id)
    if request.method == 'POST':
        form = DomainRecordForm(model=DomainRecord, instance=domain_record, data=request.POST)
        if form.is_valid():
           new_domain_record = form.save()
           return HttpResponseRedirect(reverse('cmdb:list_domain_record'))
    else:
        form = DomainRecordForm(model=DomainRecord, instance=domain_record)

    app = app_info()
    app['location'] = 'edit'
    m2m_fs = DomainRecord._meta.many_to_many
    m2m_list=[]
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app, 'm2m_list':m2m_list} ,context_instance=RequestContext(request))

@csrf_exempt #禁用csrf
def list_domain_record(request):
    model_object = DomainRecord
    template_file = 'list_data.html'
    show_field_list = [ 'domain_name',
                        'ip_record',
                        'host_name',
                        'record_type',
                        'status',]
    filter_field = 'record'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'

    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_domain_record(request, domain_record_id):
    del_res={}
    if request.method == "POST":
        del_res = del_model_data(model=DomainRecord, id=domain_record_id)

    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")


