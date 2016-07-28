#coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q

from libs.views.common import list_data, del_model_items, display_confirm_msg

from cmdb.models.ip_resource import IpResource
from cmdb.forms.ip_resource import IpResourceForm
from django.views.decorators.csrf import csrf_exempt
import json
from libs.models.common import del_model_data
from libs.models.common import del_model_data
def app_info():
    app = {
      "name" : "cmdb",
      "fun"  : "ip_resource",
      "edit_url" : 'cmdb:edit_ip_resource',
      "del_url" : 'cmdb:del_ip_resource'
    }
    return app

@csrf_exempt #禁用csrf
def add_ip_resource(request):
    if request.method == 'POST':
        form = IpResourceForm(model=IpResource, data=request.POST)
        if form.is_valid():
            new_ip_resource = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_ip_resource'))
    else:
        form = IpResourceForm(model=IpResource)
    app = app_info()
    app['location'] = 'add'
    return render_to_response('add_data.html', {'form': form, 'app':app} ,context_instance=RequestContext(request))


@csrf_exempt #禁用csrf
def edit_ip_resource(request, ip_resource_id):
    ip_resource = get_object_or_404(IpResource, pk=ip_resource_id)
    if request.method == 'POST':
        form = IpResourceForm(model=IpResource, instance=ip_resource, data=request.POST)
        if form.is_valid():
           new_ip_resource = form.save()
           return HttpResponseRedirect(reverse('cmdb:list_ip_resource'))
    else:
        form = IpResourceForm(model=IpResource, instance=ip_resource)

    app = app_info()
    app['location'] = 'edit'
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app} ,context_instance=RequestContext(request))

@csrf_exempt #禁用csrf
def list_ip_resource(request):
    model_object = IpResource
    template_file = 'list_data.html'
    show_field_list = ['idc_contract',
                       'alias',
                       'operator',
                       'begin_ip',
                       'end_ip',
                       'mask',
                       'gateway']
    filter_field = 'ip_resource_id'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'

    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_ip_resource(request, ip_resource_id):
    del_res={}
    if request.method == "POST":
        del_res = del_model_data(model=IpResource, id=ip_resource_id)


    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")


