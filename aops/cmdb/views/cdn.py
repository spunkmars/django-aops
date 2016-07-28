#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from libs.views.common import list_data, del_model_items, display_confirm_msg

from cmdb.forms.cdn import CdnForm
from cmdb.models.common import get_model_all_field_objects, get_model_relate_field, get_model_valid_fields
from cmdb.models.cdn import Cdn
import json
from libs.models.common import del_model_data

def app_info():
    app = {
        "name" : "cmdb",
        "fun"  : "cdn",
        "edit_url" : "cmdb:edit_cdn",
        "del_url" : "cmdb:del_cdn"
    }
    return app

@csrf_exempt #禁用csrf
def add_cdn(request):
    if request.method == 'POST':
        form = CdnForm(model=Cdn, data=request.POST)
        if form.is_valid():
            new_cdn = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_cdn'))
    else:
        form = CdnForm(model=Cdn
        )

    app = app_info()
    app['location'] = 'add'
    m2m_fs = Cdn._meta.many_to_many
    m2m_list=[]
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    return render_to_response('add_data.html',
                                  { 'form': form, 'app':app, 'm2m_list':m2m_list} ,context_instance=RequestContext(request))



@csrf_exempt #禁用csrf
def edit_cdn(request, cdn_id):
    cdn = get_object_or_404(Cdn, pk=cdn_id)
    if request.method == 'POST':
        form = CdnForm(model=Cdn, instance=cdn, data=request.POST)
        if form.is_valid():
           new_cdn = form.save()
           return HttpResponseRedirect(reverse('cmdb:list_cdn'))
    else:
        form = CdnForm(model=Cdn, instance=cdn)
    app = app_info()
    app['location'] = 'edit'
    m2m_fs = Cdn._meta.many_to_many
    m2m_list=[]
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app, 'm2m_list':m2m_list} ,context_instance=RequestContext(request))


@csrf_exempt #禁用csrf
def list_cdn(request):

    model_object = Cdn
    template_file = 'list_data.html'
    #show_field_list = get_model_all_field_objects(model=model_object)
    show_field_list = ['id', 'company', 'status', 'comment']
    filter_field = 'supplier' 
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'
    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_cdn(request, cdn_id):
    del_res = {}
    if request.method == "POST":
        del_res = del_model_data(model=Cdn, id=cdn_id)

    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")

