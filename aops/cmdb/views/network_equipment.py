#coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q

from libs.views.common import list_data, del_model_items, display_confirm_msg

from cmdb.models.network_equipment import NetworkEquipment
from cmdb.forms.network_equipment import NetworkEquipmentForm
from django.views.decorators.csrf import csrf_exempt
from cmdb.models.device import Device
from cmdb.forms.device import DeviceForm
import json
from django.db import IntegrityError
from libs.models.common import del_model_data
def app_info():
    app = {
      "name" : "cmdb",
      "fun"  : "network_equipment",
      "edit_url" : 'cmdb:edit_network_equipment',
      "del_url" : 'cmdb:del_network_equipment'
    }
    return app

@csrf_exempt #禁用csrf
def add_network_equipment(request):

    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST.update({
            'DEV-device_id':request.POST.get('uuid'),
            'DEV-is_dynamic':request.POST.get('is_dynamic'),
            'DEV-is_deleted':request.POST.get('is_deleted'),
            'DEV-type':'1',
        })

        form = NetworkEquipmentForm(model=NetworkEquipment, data=request.POST)
        ex_form = DeviceForm(model=Device, prefix='DEV', data=request.POST)
        if form.is_valid() and ex_form.is_valid():
            try :
                new_device = ex_form.save()
            except IntegrityError,e:
                pass
            new_network_equipment = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_network_equipment'))

    else:
        form = NetworkEquipmentForm(model=NetworkEquipment)
        ex_form = DeviceForm(model=Device,prefix='DEV',initial={'type':'physical server'})

    app = app_info()
    app['location'] = 'add'
    m2m_fs = NetworkEquipment._meta.many_to_many
    m2m_list=[]
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    return render_to_response('add_data.html',
                                  { 'form': form, 'ex_form':ex_form, 'app':app, 'm2m_list':m2m_list} ,context_instance=RequestContext(request))


@csrf_exempt #禁用csrf
def edit_network_equipment(request, network_equipment_id):
    network_equipment = get_object_or_404(NetworkEquipment, pk=network_equipment_id)
    if network_equipment:
        device_qset = Device.objects.filter(type=1, device_id=network_equipment.uuid)
        device = device_qset[0] if len(device_qset) >=1 else None
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST.update({
            'DEV-device_id':request.POST.get('uuid'),
            'DEV-is_dynamic':request.POST.get('is_dynamic'),
            'DEV-is_deleted':request.POST.get('is_deleted'),
            'DEV-type':1,
        })

        form = NetworkEquipmentForm(model=NetworkEquipment, instance=network_equipment, data=request.POST)
        if device :
            ex_form = DeviceForm(model=Device, prefix='DEV', instance=device, data=request.POST)
        else:
            ex_form = DeviceForm(model=Device, prefix='DEV',  data=request.POST)

        if form.is_valid() and ex_form.is_valid():
            try :
                new_device = ex_form.save()
            except IntegrityError,e:
                pass
            new_network_equipment = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_network_equipment'))
    else:
        form = NetworkEquipmentForm(model=NetworkEquipment, instance=network_equipment)
        if device :
            ex_form = DeviceForm(model=Device, prefix='DEV', instance=device)
        else:
            ex_form = DeviceForm(model=Device, prefix='DEV')
    app = app_info()
    app['location'] = 'edit'
    m2m_fs = NetworkEquipment._meta.many_to_many
    m2m_list=[]
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    return render_to_response('edit_data.html',
                                  { 'form': form, 'ex_form':ex_form, 'app':app, 'm2m_list':m2m_list} ,context_instance=RequestContext(request))

@csrf_exempt #禁用csrf
def list_network_equipment(request):
    model_object = NetworkEquipment
    template_file = 'list_data.html'
    show_field_list = [ 'uuid',
                        'manufacturer',
                        'brand',
                        'model_num',
                        'serial',
                        'idc_device_num',
                        'volume',
                        'asset_num',
                        'order_num',
                        'order_date',
                        'price',
                        'equipment_type',
                        'total_ports',
                        'status']

    ex_field_list = {
            'Device': {
                'filter': {
                    'st':{'type':1},
                    'dy':{'device_id':'uuid'}
                },
                'fields':['contract', 'cabinet_seat',]
            },
    }

    filter_field = 'uuid'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'

    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items,
                               filter_field = filter_field, template_file = template_file, show_field_list = show_field_list, ex_field_list = ex_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_network_equipment(request, network_equipment_id):
    del_res={}
    if request.method == "POST":
        net_instance = get_object_or_404(NetworkEquipment, pk=network_equipment_id)
        if net_instance:
            sp_relate_objects =  Device.objects.filter(Q(type=1), Q(device_id=net_instance.uuid))
            for sp_relate_object in sp_relate_objects:
                del_model_data(model=Device, id=sp_relate_object.id)
        del_res = del_model_data(model=NetworkEquipment, id=network_equipment_id)
    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")


