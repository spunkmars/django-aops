#coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q

from libs.views.common import list_data, del_model_items, display_confirm_msg

from cmdb.models.ip_record import IpRecord
from cmdb.forms.ip_record import IpRecordForm
from django.views.decorators.csrf import csrf_exempt
import json
from libs.models.common import del_model_data

def app_info():
    app = {
      "name" : "cmdb",
      "fun"  : "ip_record",
      "edit_url" : 'cmdb:edit_ip_record',
      "del_url" : 'cmdb:del_ip_record'
    }
    return app

@csrf_exempt #禁用csrf
def add_ip_record(request):
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST.update({
            'status':1,
        })
        form = IpRecordForm(model=IpRecord, data=request.POST)



        if form.is_valid():
            new_ip_record = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_ip_record'))
    else:
        form = IpRecordForm(model=IpRecord)
    app = app_info()
    app['location'] = 'add'
    return render_to_response('add_data.html', {'form': form, 'app':app} ,context_instance=RequestContext(request))


@csrf_exempt #禁用csrf
def edit_ip_record(request, ip_record_id):
    ip_record = get_object_or_404(IpRecord, pk=ip_record_id)
    if request.method == 'POST':
        form = IpRecordForm(model=IpRecord, instance=ip_record, data=request.POST)
        if form.is_valid():
           new_ip_record = form.save()
           return HttpResponseRedirect(reverse('cmdb:list_ip_record'))
    else:
        form = IpRecordForm(model=IpRecord, instance=ip_record)

    app = app_info()
    app['location'] = 'edit'
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app} ,context_instance=RequestContext(request))

@csrf_exempt #禁用csrf
def list_ip_record(request):
    model_object = IpRecord
    template_file = 'list_data.html'
    show_field_list = [
                       'ip_resource',
                       'alias',
                       'ip_address',
                       'mask',
                       'gateway',
                       'status']
    filter_field = 'ip_address'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'

    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_ip_record(request, ip_record_id):
    del_res={}
    if request.method == "POST":
        del_res = del_model_data(model=IpRecord, id=ip_record_id)

    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")


