#coding=utf-8

import re

import xlwt
import xlrd

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from libs.views.common import list_data, del_model_items, display_confirm_msg
from django.http import HttpResponseBadRequest
from django.template import RequestContext
from django.db import connection
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.translation import get_language

from django.db.models.fields import DateTimeField, DateField, TimeField, DecimalField, FloatField, IntegerField, \
                                      BigIntegerField, TextField, CharField, BooleanField, IPAddressField

from libs.common import Common
from aops.options import GLOBAL_OPTIONS
from libs.views.common import Ajax

from cmdb.forms.company import CompanyForm

from cmdb.models.company import Company
from cmdb.models.brand import Brand
from cmdb.models.cabinet import Cabinet
from cmdb.models.cabinet_seat import CabinetSeat
from cmdb.models.cdn import Cdn
from cmdb.models.contacts import Contacts
from cmdb.models.contract import Contract
from cmdb.models.device import Device
from cmdb.models.domain_name import DomainName
from cmdb.models.domain_record import DomainRecord
from cmdb.models.host import Host
from cmdb.models.idc import Idc
from cmdb.models.ip_resource import IpResource
from cmdb.models.ip_record import IpRecord
from cmdb.models.network_equipment import NetworkEquipment
from cmdb.models.physical_server import PhysicalServer



def app_info():
    app = {
        "name" : "data",
        "fun" : "export"
    }
    return app


def is_excel_text_type(obj=None):
    text_fields_cls = [IPAddressField, TextField, CharField ]
    for cls in text_fields_cls:
        if isinstance(obj, cls):
            return True
    return False


def is_excel_date_type(obj=None):
    date_fields_cls = [ DateTimeField, DateField, TimeField ]
    for cls in date_fields_cls:
        if isinstance(obj, cls):
            return True
    return False


def is_excel_number_type(obj=None):
    number_fields_cls = [ DecimalField, FloatField,  BigIntegerField, IntegerField ]
    for cls in number_fields_cls:
        if isinstance(obj, cls):
            return True
    return False


def is_excel_boolean_type(obj=None):
    boolean_fields_cls = [ BooleanField ]
    for cls in boolean_fields_cls:
        if isinstance(obj, cls):
            return True
    return False


def get_excel_type(obj=None):
    if is_excel_date_type(obj=obj):
        return 'date'
    elif is_excel_number_type(obj=obj):
        return 'number'
    elif is_excel_boolean_type(obj=obj):
        return 'boolean'
    elif is_excel_text_type(obj=obj):
        return 'text'
    else:
        return 'text'


def get_model_fields(model):
    m2m_fields = model._meta.many_to_many

    fields = [ y[0] for y in model._meta.get_fields_with_model() ]

    fields_d = {}
    for y in fields:
        fields_d[y.name] = {}
        if hasattr(y, 'related'):
            fields_d[y.name]['type'] = 'fk'
        else:
            fields_d[y.name]['type'] = 'normal'

        fields_d[y.name]['excel_type'] = get_excel_type(obj=y)
        fields_d[y.name]['obj'] = y

    for  y in m2m_fields:
        fields_d[y.name] = {}
        fields_d[y.name]['type'] = 'm2m'
        fields_d[y.name]['excel_type'] = get_excel_type(obj=y)
        fields_d[y.name]['obj'] = y

    insert_point = 3
    if len(fields) >= insert_point:
        fields[insert_point:insert_point] = m2m_fields
    else:
        fields[len(fields):len(fields)] = m2m_fields  #合并两个数组，第二个数组内容插入第一个数组后面。

    field_names = [ y.name for y in fields ]
    return (field_names, fields_d)



date_cell_style = xlwt.easyxf(  #这种方法定义样式，只能定义在循环外部，否则会报错。
       'pattern: pattern solid, fore_colour white;'
       'border:left thin, right thin, top thin, bottom thin;'
       'align: vertical center, horizontal center;',
      # num_format_str='YYYY-MM-DD hh:mm:ss' #2015-09-16 00:00:00
       num_format_str='YYYY-MM-DD'

)

cell_style = xlwt.easyxf(  #这种方法定义样式，只能定义在循环外部，否则会报错。
       'pattern: pattern solid, fore_colour white;'
       'border:left thin, right thin, top thin, bottom thin;'
       'align: vertical center, horizontal center;'
)


def get_cell_style(excel_type='text'):
    if excel_type == 'text':
        return  cell_style
    elif excel_type ==  'number':
        return  cell_style
    elif excel_type == 'date':
        return date_cell_style
    else:
        return cell_style


def trans_model_to_excel(model_name=None, fields_list=[]):
    model = eval('%s' % model_name )
    gb_op = GLOBAL_OPTIONS(trans_type='immediate')

    R_INT_CHOICES = gb_op.get_reverse_dict_option('INT_CHOICES')
    R_STATUS_CHOICES = gb_op.get_reverse_dict_option('STATUS_CHOICES')
    R_CONTRACT_CHOICES = gb_op.get_reverse_dict_option('CONTRACT_CHOICES')
    R_OPERATOR_CHOICES = gb_op.get_reverse_dict_option('OPERATOR_CHOICES')
    R_DOMAIN_RECORD_TYPE_CHOICES = gb_op.get_reverse_dict_option('DOMAIN_RECORD_TYPE_CHOICES')
    R_NETWORKING_HARDWARE_TYPE_CHOICES = gb_op.get_reverse_dict_option('NETWORKING_HARDWARE_TYPE_CHOICES')

    objs = model.objects.order_by('id').all()
    wb = xlwt.Workbook(encoding='utf-8') #创建workbook， 并定义编码。

    field_style = xlwt.easyxf( #定义标题行样式。
       'pattern: pattern solid, fore_colour yellow;' # 背景色为黄色。
       'border:right thin;'  #每个单元格右边框为细线。
        'align: vertical center, horizontal center;'  # 左右居中，上下居中。
    )

    field_row_style = xlwt.easyxf(
       'font: height 500;' #定义标题行高。
    )

    row_style = xlwt.easyxf(
       'font: height 350;'  #定义数据行高。
    )

    '''
    #单独设置样式的每样属性写法。
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 5
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True

    style = xlwt.XFStyle()
    style.pattern = pattern
    style.font = font
    '''

    ws = wb.add_sheet(ugettext(model_name), cell_overwrite_ok=True)
    field_names, fields_d = get_model_fields(model=model)
    if len(fields_list) >= 1:
        field_names = fields_list

    '''
    渲染标题行。
    '''
    i = 0
    for field_name in field_names:
        ws.write(0, i, ugettext(field_name), field_style)
        ws.col(i).width = 6000
        i = i + 1
    ws.row(0).set_style(field_row_style)

    '''
    渲染数据行。
    '''
    excel_row = 1
    for obj in objs:
        i=0
        for field_name in field_names:
            if fields_d[field_name]['type'] == 'fk':
                ws.write(excel_row, i, getattr(obj, field_name).__unicode__(),
                    get_cell_style(excel_type=fields_d[field_name]['excel_type'])
                )
            elif fields_d[field_name]['type'] == 'm2m':
                v_str = ''
                z = 1
                for x in getattr(obj, field_name).get_queryset():
                    if z == 1:
                        v_str = '%s' %  ( x.__unicode__() )
                    else:
                        v_str = '%s, %s' %  ( v_str, x.__unicode__() )
                    z = z + 1
                ws.write(excel_row, i, v_str, get_cell_style(excel_type=fields_d[field_name]['excel_type']))
            elif fields_d[field_name]['type'] == 'normal':
                field_val = None
                if field_name in ['is_dynamic', 'is_deleted', 'is_virtual_machine', 'is_run', 'is_remote_control', 'is_control_card', 'is_virtualization']:
                    field_val = R_INT_CHOICES[getattr(obj, field_name)]
                elif field_name in ['status']:
                    field_val = R_STATUS_CHOICES[getattr(obj, field_name)]
                elif field_name in ['contract_type']:
                    field_val = R_CONTRACT_CHOICES[getattr(obj, field_name)]
                elif field_name in ['operator']:
                    field_val = R_OPERATOR_CHOICES[getattr(obj, field_name)]
                elif field_name in ['record_type']:
                    field_val = R_DOMAIN_RECORD_TYPE_CHOICES[getattr(obj, field_name)]
                elif field_name in ['equipment_type']:
                    field_val = R_NETWORKING_HARDWARE_TYPE_CHOICES[getattr(obj, field_name)]
                else:
                    field_val = getattr(obj, field_name)

                ws.write(excel_row, i, field_val,
                    get_cell_style(excel_type=fields_d[field_name]['excel_type'])
                )

            i = i + 1
        ws.row(excel_row).set_style(row_style)
        excel_row = excel_row + 1

    return wb


def index(request):
    app = app_info()
    app['location'] = 'index'
    models_list = ['Company', 'Brand', 'Cabinet', 'CabinetSeat', 'Cdn', 'Contacts', 'Contract', 'Device',
                   'DomainName', 'DomainRecord', 'Host', 'Idc', 'IpResource', 'IpRecord',
                   'NetworkEquipment', 'PhysicalServer'
    ]

    return render_to_response('export/export.html',
                              {'app':app, 'models_list':models_list},
                              context_instance=RequestContext(request)
                              )


@csrf_exempt #禁用csrf
def get_model_field_list(request):
    ajax_ins = Ajax(request=request, s_method=['GET', 'POST'])
    in_data = ajax_ins.get_ds_input_data()
    model_name = in_data['model']
    da = {}
    if model_name == 'NULL':
        da = {'fields':[]}
    else:
        model = eval('%s' % model_name)
        field_names, fields_d = get_model_fields(model=model)
        field_names_l = []
        for name in field_names:
            field_names_l.append({'name':ugettext(name), 'val':name})
        da = {'fields':field_names_l}
    ajax_ins.load_data(da)
    return ajax_ins.make_response()


@csrf_exempt #禁用csrf
def export(request):
    model_name = request.POST['model']
    file_name = ugettext(model_name)
    http_user_agent = request.META['HTTP_USER_AGENT']
    s_re =  re.compile(r'MSIE')
    m = s_re.search(http_user_agent)
    is_ie_user_agent = 0
    curr_lang = get_language()
    if  hasattr(m, 'group'):
        is_ie_user_agent = 1

    if is_ie_user_agent == 1 and curr_lang == 'zh-cn':  # 使得IE在中文环境下能正常显示中文文件名。
        file_name = file_name.encode('gb2312') # utf8
    else:
        file_name = file_name.encode('utf8') # utf8, gb2312 备用

    fields_list =[]
    fields_list = request.REQUEST.getlist('fields_list')
    wb=trans_model_to_excel(model_name=model_name,fields_list=fields_list)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % file_name
    response['Set-Cookie'] = 'fileDownload=true; path=/'
    wb.save(response)
    return response





