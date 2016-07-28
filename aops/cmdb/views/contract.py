 #coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q

from libs.views.common import list_data, del_model_items, display_confirm_msg

from cmdb.models.contract import Contract
from cmdb.forms.contract import ContractForm
from django.views.decorators.csrf import csrf_exempt
import json
from libs.models.common import del_model_data

def app_info():
    app = {
      "name" : "cmdb",
      "fun"  : "contract",
      "edit_url" : 'cmdb:edit_contract',
      "del_url" : 'cmdb:del_contract'
    }
    return app

@csrf_exempt #禁用csrf
def add_contract(request):
    if request.method == 'POST':
        form = ContractForm(model=Contract, data=request.POST)
        if form.is_valid():
            new_contract = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_contract'))
    else:
        form = ContractForm(model=Contract)

    
    app = app_info()
    app['location'] = 'add'
    return render_to_response('add_data.html', {'form': form, 'app':app} ,context_instance=RequestContext(request))


@csrf_exempt #禁用csrf
def edit_contract(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if request.method == 'POST':
        form = ContractForm(model=Contract, instance=contract, data=request.POST)
        if form.is_valid():
           new_contract = form.save()
           return HttpResponseRedirect(reverse('cmdb:list_contract'))
    else:
        form = ContractForm(model=Contract, instance=contract)

    app = app_info()
    app['location'] = 'edit'
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app} ,context_instance=RequestContext(request))

@csrf_exempt #禁用csrf
def list_contract(request):

    model_object = Contract
    template_file = 'list_data.html'
    show_field_list = [ 'contract_serial',
                        'contract_name',
                        'contract_type',
                        'company',
                        'signing_time',
                        'deadline',
                        'status']
    filter_field = 'contract_serial'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'

    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_contract(request, contract_id):
    del_res={}
    if request.method == "POST":
        del_res = del_model_data(model=Contract, id=contract_id)

    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")


