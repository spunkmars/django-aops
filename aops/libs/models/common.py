#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from cmdb.models.common import get_model_all_field_objects, get_model_relate_field, get_model_valid_fields

from django.db import IntegrityError

def save_model_data(model,**kwargs):
    m2m_fields = model._meta.many_to_many
    m2m_data={}
    for m2m in m2m_fields:
        if m2m.name in kwargs:
            m2m_data[m2m.name] = kwargs[m2m.name]
            del kwargs[m2m.name]

    fk_lists = []
    for field in  model._meta.fields:
        if hasattr(field, 'related'):
            fk_lists.append(field)

    id =  kwargs.get('id',None)
    if id:
        now = model.objects.get(pk = id)
        for fk in fk_lists:
            fk_object = getattr(now, fk.name)
            if hasattr(fk_object, 'status'):
                fk_object.status = 1
                fk_object.save()

    new_instance = model(**kwargs)
    new_instance.save()


    for fk in fk_lists:
        fk_object = getattr(new_instance, fk.name)
        if hasattr(fk_object, 'status'):
            fk_object.status = 0
            fk_object.save()

    if m2m_data:
        for field in m2m_fields:
            if not field.rel.related_name:
                model_rel_field = field.related_query_name()
                exec('had_relates = [ x for x in field.rel.through.objects.filter( %s = new_instance) ]' % model_rel_field )
                tmp_relates=[]
                for data in m2m_data[field.name]:
                    try:
                        exec('rel_through_ins = field.rel.through.objects.create( %s = new_instance, %s = data)' %(model_rel_field, field.name))
                        rel_through_ins.save()
                        if hasattr(data,'status'):
                            data.status=0
                            data.save()
                        tmp_relates.append(rel_through_ins)
                    except IntegrityError as e:
                        exec('x = field.rel.through.objects.filter( %s = new_instance, %s = data)' %(model_rel_field, field.name))
                        tmp_relates += [r for r in x]
                now_relates = tmp_relates
                del_relates = list( set(had_relates).difference(set(now_relates)) )

                for rel in del_relates:
                     m2m_object = getattr(rel,field.name)
                     #print m2m_object
                     if hasattr(m2m_object, 'status'):
                         m2m_object.status = 1
                     rel.delete()


            else:
                getattr(new_instance, field.name).update(status=1)
                datas=m2m_data[field.name]
                for data in datas:
                    #print hasattr(data,'status')
                    if hasattr(data,'status'):
                        data.status=0
                        data.save()
                setattr(new_instance, field.name, m2m_data[field.name])

    return new_instance



def del_model_data(model,**kwargs):
    id =  kwargs.get('id',None)
    instance = get_object_or_404(model, pk=id)

    if instance:
        fk_lists=[]
        for field in  model._meta.fields:
            if hasattr(field, 'related'):
                fk_lists.append(field)

        for fk in fk_lists:
            fk_object = getattr(instance, fk.name)
            if hasattr(fk_object, 'status'):
                fk_object.status = 1
                #print "Change status FK:",fk_object,", Status ",fk_object.status,"\n"
                fk_object.save()


        m2m_fields = model._meta.many_to_many

        for m2m_field in m2m_fields:
            m2m_datas = getattr(instance, m2m_field.name)
            for m2m_object in m2m_datas.get_queryset():
                if hasattr(m2m_object, 'status'):
                    m2m_object.status = 1
                    #print "Change status M2M:",m2m_object,", Status ",m2m_object.status
                    m2m_object.save()
                try:
                    m2m_datas.remove(m2m_object)
                except AttributeError,e:
                    exec("m2m_datas.through.objects.get(%s=m2m_object).delete()" % m2m_datas.target_field.name)
                    if rel_object:
                        rel_object.delete()

        res=0
        meg='Delete Success !'
        instance.delete()
        #print "Instance Delete"
    else:
        res=1
        meg='Delete Failed !'

    del_res={
         'res' : res,
         'meg' : meg
    }
    return del_res


