#coding=utf-8
from django.db import models

def get_model_all_field_objects(model=None):
    field_objects = []
    if model is not None:
        field_objects = [ y[0] for y in model._meta.get_fields_with_model() ]
    return field_objects


def get_model_relate_field(model=None):
    field_objects = get_model_all_field_objects(model=model) #取得model中的全部field 对象
    relate_field = {}
    for field in field_objects:
        if hasattr(field, 'related') :  #判断是否为外键。
            relate_field[field.name] = field.related.parent_model
    return relate_field



def get_model_valid_fields(model=None, invalid_fields=[]):
    valid_fields = []
    field_objects = get_model_all_field_objects(model=model)
    for field in field_objects:
        single_field = {}
        if field.editable == False or field.unique == True :    #过滤 不允许修改, 不允许重复  的field 
            continue
        if field.has_default():
            field_init = field.default
        else:
            field_init = None
        #if field.verbose_name:
        #    field_name = field.verbose_name
        #else:
        #    field_name = field.name
        field_name = field.name
        single_field['name'] = field_name
        single_field['init'] = field_init
        single_field['obj'] = field
        if len(single_field) >= 3 and single_field['name'] not in invalid_fields:
            valid_fields.append(single_field)
    return valid_fields

