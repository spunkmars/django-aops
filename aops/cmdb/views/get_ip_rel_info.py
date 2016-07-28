#coding=utf-8

import pprint
import json
import time
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from cmdb.models.host import  Host,PhysicalServer
from cmdb.models.network_equipment import  NetworkEquipment
from cmdb.models.idc_contract import IdcContract,Idc
from cmdb.models.ip_record import  IpRecord,IpResource
from django.db.models import Q,ObjectDoesNotExist


import ipaddr
def DD(vars):
    pprint.pprint(vars)


@csrf_exempt #禁用csrf
def search_ip_resource(**kwargs):
    return_json={'status':1, 'error':'No post data'}
    if kwargs:
        u_data = kwargs
    else:
        return  return_json

    area = u_data.get("area", u'广州')
    target_ip= u_data.get("ip",None)
    if not target_ip:
        return  return_json

    idc_objects = Idc.objects.filter(idc_name__contains=area)
    rel_objects = IdcContract.objects.filter(idc__in = [ x for x in idc_objects.values_list("id") ])
    if rel_objects:
        ids =  [ x[0] for x in rel_objects.values_list("id") ]

    ip_resources = IpResource.objects.filter(idc_contract__in = ids)

    return_json={
        'ids':[],
        'status':1,
    }

    for ip_resource in ip_resources:
        if ip_resource.operator == "lan":
            mask = "255.255.255.0"
        else:
            mask = ip_resource.mask

        ip_range = "%s/%s" % (ip_resource.begin_ip,mask)
        end_ip = "%s" % ip_resource.end_ip
        end_ip_object = ipaddr.IPAddress(end_ip)
        ip_network = ipaddr.IPNetwork(ip_range)
        ip_list = [ x.__str__() for x in  ip_network.iterhosts() if x._ip <= end_ip_object._ip ]
        if target_ip in ip_list:
            return_json['ids'].append(ip_resource.id)
            return_json['status'] = 0
    return  return_json

@csrf_exempt #禁用csrf
def get_ip_resource(request):
    u_data={}
    if request.body:
        u_data=json.loads(request.body)

    return_str = search_ip_resource(**u_data)
    return_str = json.dumps(return_str)
    return HttpResponse(return_str, content_type="text/html")



@csrf_exempt #禁用csrf
def search_rel_ip_obj(**kwargs):
    u_data = kwargs
    ip = u_data.get("ip",None)
    area = u_data.get("area",u"广州")
    model_name_list = u_data.get("model","PhysicalServer").split(":")
    model_name = model_name_list[0]
    real_model = model_name_list[1] if model_name_list[1] else None
    exec("model=%s" % model_name)
    if ip:
        res_status = search_ip_resource(**u_data)
        record_range = []
        if res_status["status"] == 0:
            for ip_resource_id in res_status["ids"]:
                try:
                    ip_obj = IpRecord.objects.get(ip_resource=ip_resource_id, ip_address=ip)
                    rel_obj = model.ip_record.through.objects.get(iprecord=ip_obj)
                    model_obj = getattr(rel_obj,model_name.lower())
                    if real_model :
                        exec("r_model=%s" % real_model)
                        model_obj = r_model.objects.get(serial=model_obj.serial)
                    record_range.append({"%d-%s" % (ip_resource_id,ip):model_obj.id})
                except ObjectDoesNotExist , e:
                    print e.message
    else:
        record_range = [{"%d-%s" %( j.ip_resource.id,j.ip_address):x.id} for x in model.objects.all() for j in  x.ip_record.all()]
    return_str=json.dumps(record_range)
    return return_str

@csrf_exempt #禁用csrf
def get_ip_rel_info(request):
    u_data={}
    if request.body:
        u_data=json.loads(request.body)

    return_str = search_rel_ip_obj(**u_data)
    return_str = json.dumps(return_str)
    return HttpResponse(return_str, content_type="text/html")