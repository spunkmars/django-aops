#coding=utf-8

import sys
if  sys.version_info >= (2, 6, 0):
    import json as json
else:
    import simplejson as json


from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext


from libs.data_serialize import DataSerialize

from aops.options import GLOBAL_OPTIONS

from cmdb.models.physical_server  import PhysicalServer
from cmdb.models.cabinet import Cabinet
from cmdb.models.cabinet_seat import CabinetSeat
from cmdb.models.host import Host
from cmdb.models.network_equipment import NetworkEquipment
from cmdb.models.idc import Idc
from cmdb.models.idc_contract import  IdcContract
from cmdb.models.device import Device


from libs.views.common  import Ajax


def app_info():
    app = {
      "name" : "aops",
      "fun"  : "dashboard",
    }
    return app



@csrf_exempt #禁用csrf
def dashboard(request):
    app = app_info()
    app['location'] = 'dashboard'
    return render_to_response('dashboard.html',
                                  { 'app':app}, context_instance=RequestContext(request))


def get_models_info(models_obj):
    models_obj = models_obj
    gb_op = GLOBAL_OPTIONS(trans_type='immediate')
    O_STATUS_CHOICES = gb_op.get_dict_option('STATUS_CHOICES')
    v_info = {}
    v_info['total'] = models_obj.objects.count()
    v_info['status'] = {}
    filter_field = 'status'
    query = 0
    status_choices_dict = O_STATUS_CHOICES
    for s_key in status_choices_dict:
        v_info['status'][s_key] = len(  models_obj.objects.filter(eval( "Q(%s__contains=\"%s\")" % (filter_field, status_choices_dict[s_key]) )) )

    return v_info


@csrf_exempt #禁用csrf
def dashboard_ajax(request):
    ajax_ins = Ajax(request=request, s_method=['POST'], ds=DataSerialize(format='json', ensure_ascii =True))
    in_data = ajax_ins.get_ds_input_data()

    physical_server_info = get_models_info(PhysicalServer)
    host_info = get_models_info(Host)
    cabinet_info = get_models_info(Cabinet)
    networkEquipment_info = get_models_info(NetworkEquipment)


    idc_ins = Idc.objects.all()
    idc_dict = {}
    for idc_i  in  idc_ins:
        idc_dict[idc_i.idc_name] = idc_i.id

    idc_info = {}
    idc_info['cabinet'] = {}

    cabinet_ins = Cabinet.objects.all()
    cabinet = []
    for cabinet_i in cabinet_ins:
        idc_name = cabinet_i.idc_contract.idc.idc_name
        cabinet.append(
            {
                'name':cabinet_i.cabinet_name,
                'id':cabinet_i.id,
                'idc_contract_id':cabinet_i.idc_contract.id,
                'idc_id':cabinet_i.idc_contract.idc.id,
                'idc_name':idc_name,
            }
        )

        if idc_name in idc_info['cabinet']:
           idc_info['cabinet'][idc_name] = idc_info['cabinet'][idc_name] + 1
        else:
           idc_info['cabinet'][idc_name] = 1


    device = []
    dev_ins = Device.objects.all()
    for dev_i in dev_ins:
        cabinet_id = dev_i.cabinet_seat.cabinet.id
        idc_id = None
        idc_name = None
        for cabinet_v in cabinet:
            if cabinet_v['id'] == cabinet_id:
                idc_id = cabinet_v['idc_id']
                idc_name = cabinet_v['idc_name']
                break

        device.append(
            {
                'uuid':dev_i.device_id,
                'cabinet_seat_id': dev_i.cabinet_seat.id,
                'cabinet_seat_location':dev_i.cabinet_seat.cabinet_seat_location,
                'cabinet_name':dev_i.cabinet_seat.cabinet.cabinet_name,
                'cabinet_id':cabinet_id,
                'idc_id':idc_id,
                'idc_name':idc_name,
            }
        )


    idc_info['physical_server'] = {}
    physical_server_ins = PhysicalServer.objects.all()
    physical_server = []
    for p_s_i in physical_server_ins:
        uuid = p_s_i.uuid
        device_i = {}
        for device_v in device:
            if device_v['uuid'] == uuid:
                device_i = device_v
                break

        if len(device_i) < 1:
            continue

        physical_server.append(
            {
                'uuid':uuid,
                'id':p_s_i.id,
                'device':device_i,
                'idc_name':device_i['idc_name'],
                'idc_id':device_i['idc_id'],
            }
        )

        if device_i['idc_name'] in  idc_info['physical_server']:
            idc_info['physical_server'][device_i['idc_name']] = idc_info['physical_server'][device_i['idc_name']] + 1
        else:
            idc_info['physical_server'][device_i['idc_name']] = 1


    idc_info['network_quipment'] = {}
    network_quipment_ins = NetworkEquipment.objects.all()
    network_quipment = []
    for e_q_i in network_quipment_ins:
        uuid = e_q_i.uuid
        device_i = {}
        for device_v in device:
            if device_v['uuid'] == uuid:
                device_i = device_v
                break

        if len(device_i) < 1:
            continue

        network_quipment.append(
            {
                'uuid':uuid,
                'id':e_q_i.id,
                'device':device_i,
                'idc_name':device_i['idc_name'],
                'idc_id':device_i['idc_id'],
            }
        )

        if device_i['idc_name'] in  idc_info['network_quipment']:
            idc_info['network_quipment'][device_i['idc_name']] = idc_info['network_quipment'][device_i['idc_name']] + 1
        else:
            idc_info['network_quipment'][device_i['idc_name']] = 1


    idc_info['host'] = {}
    host_ins = Host.objects.all()
    host = []
    for host_i in host_ins:
        physical_server_id = host_i.physical_server.id
        physical_server_v = {}
        for p_s_v in  physical_server:
            if p_s_v['id'] == physical_server_id:
                physical_server_v = p_s_v
                break

        if len(physical_server_v) < 1:
            continue

        host.append({'id':host_i.id, 'uuid': host_i.uuid, 'idc_id':physical_server_v['idc_id'], 'idc_name':physical_server_v['idc_name'] })

        if physical_server_v['idc_name'] in idc_info['host']:
            idc_info['host'][physical_server_v['idc_name']] = idc_info['host'][physical_server_v['idc_name']] + 1
        else:
            idc_info['host'][physical_server_v['idc_name']] = 1


    ugettext('PhysicalServer'), ugettext('Host'), ugettext('NetworkEquipment'), ugettext('Cabinet')

    ebc1_dict = {
        'PhysicalServer': 'physical_server',
        'Host':'host',
        'NetworkEquipment':'network_quipment',
        'Cabinet':'cabinet'
    }

    ebc1_x_category = []
    ebc1_keys = []
    for dv in ebc1_dict:
        ebc1_x_category.append( ugettext(dv) )
        ebc1_keys.append(dv)

    ebc1_series = []
    for idc_d in idc_dict:
        idc_v = []
        for dv in ebc1_keys:
            if idc_d not in idc_info[ebc1_dict[dv]]:
                idc_info[ebc1_dict[dv]][idc_d] = 0
            idc_v.append( idc_info[ebc1_dict[dv]][idc_d] )

        ebc1_series.append({'name':idc_d, 'stack':'总量', 'data':idc_v})


    mbc1 = {
        'chart_id': 'morris-bar-chart01',
        's_title': ugettext('Asset'),
        'data': {
            ugettext('PhysicalServer'): physical_server_info['total'],
            ugettext('Host'): host_info['total'],
            ugettext('NetworkEquipment'): networkEquipment_info['total'],
            ugettext('Cabinet'): cabinet_info['total'],
            }
    }

    ebc2 = {
        'chart_id': 'morris-bar-chart04',
        's_title': ugettext('Application Geographical Distribution'),
        'data': {
            'x_category': ['tomcat',  'mysql', 'postgresql', 'nginx', 'apache', 'redis', 'memcached', 'php', 'rabbitmq', 'logstash', 'zabbix'],
            'series': [
                {
                    'name': '机房1',
                    'stack': '总量',
                    'data': [3000, 310, 200, 300, 50, 2000, 208, 2, 30, 65, 1]
                },
                {
                    'name': '机房2',
                    'stack': '总量',
                    'data': [800, 105, 80, 100, 20, 500, 201, 1, 32, 25, 1]
                },
                {
                    'name': '机房3',
                    'stack': '总量',
                    'data': [20, 15, 0, 3, 2, 0, 0, 0, 0, 0, 1]
                },
                {
                    'name': '机房4',
                    'stack': '总量',
                    'data': [5, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1]
                },
            ]
         },
    }



    ebc1 = {
        'chart_id': 'morris-bar-chart03',
        's_title': ugettext('Assets Geographical Distribution'),
        'data': {
            'x_category': ebc1_x_category,
            'series': ebc1_series,
         },
    }


    mbc2 = {
        'chart_id': 'morris-bar-chart02',
        's_title': ugettext('Application'),
        'data': {
            'tomcat':3800,
            'mysql':415,
            'postgresql':280,
            'nginx':400,
            'apache':70,
            'redis':2500,
            'memcached':409,
            'php':4,
            'rabbitmq':55,
            'logstash':90,
            'zabbix':4
            }
    }

    mdc1 = {
        'chart_id': 'morris-donut-chart01',
        's_title': ugettext('PhysicalServer'),
        'data':physical_server_info['status'],
    }


    mdc2 = {
        'chart_id': 'morris-donut-chart02',
        's_title': ugettext('NetworkEquipment'),
        'data': networkEquipment_info['status'],
    }

    mdc3 = {
        'chart_id': 'morris-donut-chart03',
        's_title': ugettext('Host'),
        'data': host_info['status'],
    }


    mdc4 = {
        'chart_id': 'morris-donut-chart04',
        's_title': ugettext('Cabinet'),
        'data': cabinet_info['status'],
    }

    mdc = [mdc1, mdc2, mdc3, mdc4]
    mbc = [mbc1, mbc2]
    ebc = [ebc1, ebc2]
    md = {'mdc':mdc, 'mbc':mbc, 'ebc':ebc}
    #ajax_ins.DD(md)
    ajax_ins.load_data(md)
    return ajax_ins.make_response()
