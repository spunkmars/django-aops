#coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q

from libs.views.common import list_data, del_model_items, display_confirm_msg

from cmdb.models.domain_name import DomainName
from cmdb.forms.domain_name import DomainNameForm
from django.views.decorators.csrf import csrf_exempt
import json
from libs.models.common import del_model_data

def app_info():
    app = {
      "name" : "cmdb",
      "fun"  : "domain_name",
      "edit_url" : 'cmdb:edit_domain_name',
      "del_url" : 'cmdb:del_domain_name'
    }
    return app

@csrf_exempt #禁用csrf
def add_domain_name(request):
    if request.method == 'POST':
        form = DomainNameForm(model=DomainName, data=request.POST)
        if form.is_valid():
            new_domain_name = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_domain_name'))
    else:
        form = DomainNameForm(model=DomainName)
    app = app_info()
    app['location'] = 'add'
    return render_to_response('add_data.html', {'form': form, 'app':app} ,context_instance=RequestContext(request))


@csrf_exempt #禁用csrf
def edit_domain_name(request, domain_name_id):
    domain_name = get_object_or_404(DomainName, pk=domain_name_id)
    if request.method == 'POST':
        form = DomainNameForm(model=DomainName, instance=domain_name, data=request.POST)
        if form.is_valid():
           new_domain_name = form.save()
           return HttpResponseRedirect(reverse('cmdb:list_domain_name'))
    else:
        form = DomainNameForm(model=DomainName, instance=domain_name)

    app = app_info()
    app['location'] = 'edit'
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app} ,context_instance=RequestContext(request))

@csrf_exempt #禁用csrf
def list_domain_name(request):
    model_object = DomainName
    template_file = 'list_data.html'
    show_field_list = [ 'contract',
                         'name',
                         'supplier',
                         'resolution_supplier',
                         'application_date',
                         'deadline',
                         'status' ]
    filter_field = 'domain_name_id'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'

    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_domain_name(request, domain_name_id):
    del_res={}
    if request.method == "POST":
        del_res = del_model_data(model=DomainName, id=domain_name_id)

    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")


