#coding=utf-8


import pprint
import json
import time
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from cmdb.models.physical_server import  PhysicalServer
from cmdb.forms.physical_server import  PhysicalServerForm

from cmdb.models.ip_record import  IpRecord
from cmdb.forms.ip_record import  IpRecordForm

from cmdb.models.network_equipment import  NetworkEquipment
from cmdb.forms.network_equipment import  NetworkEquipmentForm

from cmdb.models.cabinet import  Cabinet
from cmdb.forms.cabinet import  CabinetForm

from cmdb.models.cabinet_seat import  CabinetSeat
from cmdb.forms.cabinet_seat import  CabinetSeatForm

from cmdb.models.device import  Device
from cmdb.forms.device import DeviceForm

from cmdb.models.host import  Host
from cmdb.forms.host import HostForm


from django.db.models import Q


def DD(vars):
    pprint.pprint(vars)

def create_uuid(*args):
    from hashlib import md5
    id = md5()
    timestamp=time.time()
    id.update('%s%f'% (''.join(args).encode('utf8') ,timestamp))
    id = id.hexdigest()[8:-8].upper()
    return id











