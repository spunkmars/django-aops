#coding=utf-8


import json
import time

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from aops.settings import SALT_SP_KEY
from cmdb.forms.host import HostForm
from cmdb.models.host import Host
from cmdb.utils.common import create_uuid
from libs.models.common import del_model_data
from libs.salt.saltid import salt
from libs.views.common import list_data, Ajax


def app_info():
    app = {
      "name" : "cmdb",
      "fun"  : "host",
      "edit_url" : 'cmdb:edit_host',
      "del_url" : 'cmdb:del_host'
    }
    return app

@csrf_exempt #禁用csrf
def add_host(request):
    if request.method == 'POST':
        form = HostForm(model=Host, data=request.POST)
        if form.is_valid():
            new_host = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_host'))
    else:
        form = HostForm(model=Host)
    app = app_info()
    app['location'] = 'add'
    m2m_fs = Host._meta.many_to_many
    m2m_list=[]
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    return render_to_response('add_data.html',
                                  { 'form': form, 'app':app, 'm2m_list':m2m_list} ,context_instance=RequestContext(request))



@csrf_exempt #禁用csrf
def edit_host(request, host_id):
    host = get_object_or_404(Host, pk=host_id)
    if request.method == 'POST':
        form = HostForm(model=Host, instance=host, data=request.POST)
        if form.is_valid():
           new_host = form.save()
           return HttpResponseRedirect(reverse('cmdb:list_host'))
    else:
        form = HostForm(model=Host, instance=host)

    app = app_info()
    app['location'] = 'edit'
    m2m_fs = Host._meta.many_to_many
    m2m_list=[]
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app, 'm2m_list':m2m_list} ,context_instance=RequestContext(request))

@csrf_exempt #禁用csrf
def list_host(request):
    model_object = Host
    template_file = 'list_data.html'
    show_field_list = [ 'physical_server',
                        'uuid',
                        'salt_id',
                        'operating_system',
                        'system_name',
                        'roles',
                        'status']
    filter_field = 'uuid'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'

    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_host(request, host_id):
    del_res={}
    if request.method == "POST":
        del_res = del_model_data(model=Host, id=host_id)

    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")


@csrf_exempt #禁用csrf
def get_salt_id(request):
    ajax_ins = Ajax(request=request, s_method=['GET', 'POST'])
    in_data = ajax_ins.get_ds_input_data()
    d_type = in_data['d_type']
    da = {}
    if d_type == 'NULL':
        da = {'val':''}
    else:
        salt_ins=salt()
        timestamp=time.time()
        da = {'val':salt_ins.create(SALT_SP_KEY, timestamp)}
    ajax_ins.load_data(da)
    return ajax_ins.make_response()


@csrf_exempt #禁用csrf
def get_uuid(request):
    ajax_ins = Ajax(request=request, s_method=['GET', 'POST'])
    in_data = ajax_ins.get_ds_input_data()
    d_type = in_data['d_type']
    da = {}
    if d_type == 'NULL':
        da = {'val':''}
    else:
        da = {'val':create_uuid()}
    ajax_ins.load_data(da)
    return ajax_ins.make_response()