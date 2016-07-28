#coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q

from libs.views.common import list_data, del_model_items, display_confirm_msg

from cmdb.models.idc import Idc
from cmdb.models.contract import Contract
from cmdb.forms.idc import IdcForm
from django.views.decorators.csrf import csrf_exempt
import json
from libs.models.common import del_model_data

def app_info():
    app = {
      "name" : "cmdb",
      "fun"  : "idc",
      "edit_url" : 'cmdb:edit_idc',
      "del_url" : 'cmdb:del_idc'
    }
    return app

@csrf_exempt #禁用csrf
def add_idc(request):
    if request.method == 'POST':
        form = IdcForm(model=Idc, data=request.POST)
        if form.is_valid():
            new_idc = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_idc'))
    else:
        form = IdcForm(model=Idc)
    app = app_info()
    app['location'] = 'add'

    m2m_fs = Idc._meta.many_to_many
    m2m_list=[]
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    return render_to_response('add_data.html', {'form': form, 'app':app,'m2m_list':m2m_list} ,context_instance=RequestContext(request))


@csrf_exempt #禁用csrf
def edit_idc(request, idc_id):
    idc = get_object_or_404(Idc, pk=idc_id)
    if request.method == 'POST':
        form = IdcForm(model=Idc, instance=idc, data=request.POST)
        if form.is_valid():
           new_idc = form.save()
           return HttpResponseRedirect(reverse('cmdb:list_idc'))
    else:
        form = IdcForm(model=Idc, instance=idc)

    app = app_info()
    app['location'] = 'edit'

    m2m_fs = Idc._meta.many_to_many
    m2m_list=[]
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app, 'm2m_list':m2m_list} ,context_instance=RequestContext(request))

@csrf_exempt #禁用csrf
def list_idc(request):
    model_object = Idc
    template_file = 'list_data.html'
    show_field_list = ['contract',
                       'idc_name',
                       'idc_address',
                       'company',
                       'status']
    filter_field = 'idc_name'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'

    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_idc(request, idc_id):
    del_res={}
    if request.method == "POST":
        del_res = del_model_data(model=Idc, id=idc_id)

    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")

