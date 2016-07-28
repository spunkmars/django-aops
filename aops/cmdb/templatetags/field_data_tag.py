#coding=utf-8

from django import template
from django.core.urlresolvers import reverse

from django.shortcuts import render_to_response, get_object_or_404
from aops.settings import STATUS_CHOICES, CONTRACT_CHOICES, INT_CHOICES, OPERATOR_CHOICES
from libs.views.common import map_value
from cmdb.models.device import Device
register = template.Library()

def do_filed_data_analysis(parser, token):
    try:
        tag_name, object_data, object_show_fields, object_ex_fields = token.split_contents()
    except:
        raise template.TemplateSyntaxError, "%r tags error" % token.split_contents()[0]

    return FieldDataNode(object_data, object_show_fields, object_ex_fields)




class FieldDataNode(template.Node):
    def __init__(self, object_data, object_show_fields, object_ex_fields):
        self.object = template.Variable(object_data)
        self.show_fields = template.Variable(object_show_fields)
        self.ex_fields = template.Variable(object_ex_fields)

    def render(self, context):
        object = self.object.resolve(context)
        show_fields = self.show_fields.resolve(context)
        ex_fields = self.ex_fields.resolve(context)
        model = type(object)
        model_m2m_fs = model._meta.many_to_many

        data={}
        f_keys=[]
        for field,value in object.items():
            data[field.name]="none"
            if field.name == "status":
                data[field.name]=map_value(value,STATUS_CHOICES)

            elif field.name == "contract_type":
                data[field.name]=map_value(value,CONTRACT_CHOICES)

            elif field.name == "operator":
                data[field.name]=map_value(value,OPERATOR_CHOICES)

            else:
                if hasattr(field, 'related') :
                    data[field.name]=getattr(object,field.name)
                    f_keys.append(field.name)
                else:
                    data[field.name]=value


        for m2m_field in model_m2m_fs:
            m2m_datas=getattr(object,'%s' % m2m_field.name).all()
            data[m2m_field.name] = data.get(m2m_field.name,[])
            for m2m in m2m_datas:
                data[m2m_field.name].append(m2m.__unicode__())
            data[m2m_field.name]=",".join(data[m2m_field.name])

        ex_data={}
        for ex_key in ex_fields:
            ex_model = eval('%s' % ex_key)
            ex_filter=ex_fields[ex_key]['filter']
            f_words=[]
            for ft in  ex_filter:
                for k in ex_filter[ft]:
                    if ft == 'st':
                        f_words.append('%s=%s' % (k,ex_filter[ft][k]))
                    elif ft == 'dy':
                        f_words.append('%s=object.%s' % (k,ex_filter[ft][k]))
            exec("ex_qset=ex_model.objects.filter(%s)" %  ','.join(f_words))

            for fl in ex_fields[ex_key]['fields']:
                if not ex_key in ex_data:
                    ex_data[ex_key] = {}
                if ex_qset:
                    ex_data[ex_key].update({ fl : getattr(ex_qset[0], fl)})
                else:
                    ex_data[ex_key].update({ fl :"None"})

        res_str=""

        for ex_key in ex_data:
            for fl in ex_fields[ex_key]['fields']:
                    res_str=u"%s<td>%s</td>" % (res_str,ex_data[ex_key][fl])

        for key in show_fields:
            if key in data:
                #print "K:%s,V:%s" % (key,data[key])
                field_o = getattr(object, key)
                if key in f_keys and hasattr(field_o, 'get_absolute_url'):
                    res_str=u"%s<td><a href=%s >%s</a></td>" % (res_str, field_o.get_absolute_url(),data[key])
                else:
                    res_str=u"%s<td>%s</td>" % (res_str,data[key])
            else:
                res_str=u"%s<td>%s</td>" % (res_str,"None")


        return res_str
register.tag('field_data', do_filed_data_analysis)
