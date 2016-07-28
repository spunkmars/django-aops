#coding=utf-8

import copy
from itertools import chain

from django.db.models.fields import BLANK_CHOICE_DASH
from django import forms
from django.forms.util import ErrorList
from django.db.models import Q
from django.db import models
from datetime import datetime

from libs.common import Common
from libs.forms.field import TreeSelect
from libs.models.common import save_model_data

co = Common()


def set_select_choice( choices=None, select_choice=None):
    new_choices = []
    for (choice_value, choice_name) in choices:
        if choice_value != select_choice:
            new_choices.append((choice_value, choice_name))
        else:
            new_choices.insert(0, (choice_value, choice_name))
    return  new_choices

def get_year_list(*args):
    begin_year = args[0]
    end_year = args[1] + 1
    years = []
    for i in range(begin_year, end_year):
        years.append(i)
    return years

EXPIRATION_YEAR_CHOICES = get_year_list(2010, 2110)


class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return u''
        return ','.join([u'<div class="error col-sm-3 fe ">%s</div>' %e for e in self])


class newModelForm(forms.Form):

    def __init__(self, *args, **kwargs):
        files=None
        auto_id='id_%s'
        prefix=kwargs.get('prefix', None)
        self.instance = kwargs.get('instance', None)
        self.model = kwargs.get('model', None)
        initial = kwargs.get('initial', None)
        self.pre_init = kwargs.get('pre_init', None) # 开启，存储预设值功能。
        self.pre_init_done = []
        self.change = 0
        if self.model == None:
            raise
        if self.instance == None:
            instance = self.instance
            object_data = initial
        else:
            instance = self.instance
            object_data = self.get_object_data(instance)
        self.data = kwargs.get('data', None)
        data = self.data
        #error_class=ErrorList
        error_class=DivErrorList
        label_suffix=':'
        empty_permitted=False
        super(newModelForm, self).__init__(data, files, auto_id, prefix, object_data,
                                            error_class, label_suffix, empty_permitted)
        self.init_field()


    def init_field(self):
        #print self.instance
        if self.instance:
            self.id = forms.CharField(max_length=255, label='ID', widget=forms.HiddenInput())
            #print self.id
            self.init_edit_form()
        self.init_choices_and_foreign_field()
        self.init_after()

    def init_edit_form(self):
        pass


    def init_after(self):
        #填充 预设功能提供的 值。
        if self.pre_init is not None and isinstance(self.pre_init, dict):
            local_field_objects = self.get_local_field_objects(model=self.model)
            m2m_fields = [ m2m.name for m2m in self.model._meta.many_to_many ]
            self.pre_init_done.extend(m2m_fields)
            for field in local_field_objects:
                if field.name in self.pre_init_done:
                    continue
                else:
                    if field.name in self.pre_init:
                        self.fields[field.name] = self.pre_init[field.name]


    def init_treeselect_field(self, field_name=None, parent=None):
        parent_id = None
        parent = parent
        if parent is None:
            parent_id = self.id
        else:
            parent_id = parent.id
        self.fields[field_name].widget.s_choices = [ parent_id ]


    def init_choices_and_foreign_field(self):
        #对choices 及外键的field进行初始化数据
        self.local_field_objects = self.get_local_field_objects(model=self.model)
        #print self.local_field_objects
        for field in self.local_field_objects:
            if hasattr(field, 'choices') and len(field.choices) > 0 :
                if self.instance :
                    self.fields[field.name].choices =  self.get_choices(choices_type='choices', select_choice=getattr(self.instance, field.name), field_object=field)
                else:
                    if self.pre_init is not None and isinstance(self.pre_init, dict) and field.name in self.pre_init:
                        self.pre_init_done.append(field.name)
                        self.fields[field.name].choices = self.get_choices(choices_type='choices', select_choice=self.pre_init[field.name], field_object=field)
                    else:
                        if field.has_default():
                            self.fields[field.name].choices = self.get_choices(choices_type='choices', select_choice=field.get_default(), field_object=field)
                        else:
                            self.fields[field.name].choices = field.get_choices()
            elif hasattr(field, 'related'):
                if self.instance :
                    if isinstance(self.fields[field.name].widget, TreeSelect): #判断特定类型，添加自定义变量，赋值所选id进去。
                        parent = getattr(self.instance, field.name)
                        self.init_treeselect_field(field_name=field.name, parent=parent)
                    self.fields[field.name].choices =  self.get_choices(choices_type='foreign_key', filter_status=self.fields[field.name].filter_status, select_choice=getattr(self.instance, field.name), field_object=field)
                else:
                    select_choice = ''
                    # 判断是否有预设值，并且是字典类型。
                    if self.pre_init is not None and isinstance(self.pre_init, dict) and field.name in self.pre_init:
                        self.pre_init_done.append(field.name)
                        if isinstance(self.fields[field.name].widget, TreeSelect): #判断特定类型，添加自定义变量，赋值所选id进去。
                            parent = self.pre_init[field.name]
                            self.init_treeselect_field(field_name=field.name, parent=parent)
                        select_choice = self.pre_init[field.name]
                    self.fields[field.name].choices = self.get_choices(choices_type='foreign_key', filter_status=self.fields[field.name].filter_status, select_choice=select_choice, field_object=field)
            elif hasattr(field, 'default'):
                if self.instance :
                    self.fields[field.name].initial = getattr(self.instance, field.name)
                else:
                    self.fields[field.name].initial = field.get_default()

        self.m2m_field_objects=[]
        for m2m in self.model._meta.many_to_many:
            if m2m.name in self.fields.keys():
                self.m2m_field_objects.append(m2m)

        for m2m_field in self.m2m_field_objects:
            if self.instance :
                filter_queryset = self.fields[m2m_field.name].queryset
                self_queryset = getattr(self.instance, m2m_field.name).all()
                self.fields[m2m_field.name].queryset = filter_queryset | self_queryset
                self.fields[m2m_field.name].initial = self_queryset


    def get_local_field_objects(self, model=None):
        local_field_objects = []
        if model:
            local_field_objects = [ y[0] for y in model._meta.get_fields_with_model() if y[0].name in self.fields.keys() ]
        return local_field_objects


    def get_choices(self, choices_type='choices', filter_status=None, select_choice=None, field_object=None):
        new_CHOICES = []
        if choices_type == 'foreign_key'  and field_object:
            if not filter_status is None:
                pk_list = [ pk_value[0] for pk_value in field_object.related.parent_model.objects.exclude(status=filter_status).values_list('id') ]
                if self.instance:
                    pk_list.append(getattr(self.instance,field_object.name).id)
            else:
                pk_list = [ pk_value[0] for pk_value in field_object.related.parent_model.objects.all().values_list('id') ]
            #外键模型modle里必须有方法__unicode__ ，要不然会报错！
            related_instance_choices = [ (pk_value, field_object.related.parent_model.objects.get( pk=pk_value).__unicode__() ) for pk_value in pk_list ]
            if select_choice:
                new_CHOICES = set_select_choice( choices=related_instance_choices, select_choice=select_choice.id)
            else:
                related_instance_choices = BLANK_CHOICE_DASH + list(related_instance_choices)
                new_CHOICES = set_select_choice( choices=related_instance_choices, select_choice='')

        elif choices_type == 'choices'  and field_object:
            if select_choice:
                new_CHOICES = set_select_choice( choices=field_object.choices, select_choice=select_choice)
            else:
                new_CHOICES = set_select_choice( choices=BLANK_CHOICE_DASH+list(field_object.choices), select_choice='')

        return  copy.deepcopy(new_CHOICES)


    def get_object_data(self, model_instance=None):
        #related_fields = [ x.var_name for x in model_instance._meta.get_all_related_objects() ]
        #model_fields = [ k for k in model_instance._meta.get_all_field_names() if  k not in  related_fields ]
        model_fields = [ y[0].name for y in model_instance._meta.get_fields_with_model() ] #这种方法更简便！！
        data = {}
        for keys in model_fields:
            data[keys] = getattr(model_instance, keys)
        return data


    def check_field_value_unique(self, field_name=None):
        try:
            self.model.objects.get(eval( "Q(%s=\"%s\")" % (field_name, self.cleaned_data[field_name]) ))
        except self.model.DoesNotExist:
            if self.change == 0 :
                self.change = 1
            return self.cleaned_data[field_name]
        raise forms.ValidationError("This %s (%s) is already in use. Please choose another." % (field_name, self.cleaned_data[field_name]) )


    def check_field(self, field_name=None):
        if field_name and self.instance == None : 
            if self.cleaned_data.has_key(field_name) and self.cleaned_data[field_name] !='' :
                return self.check_field_value_unique(field_name=field_name)
            else:
                raise forms.ValidationError("The field [%s] can not be empty! " % field_name)
        elif field_name:
            if self.cleaned_data[field_name] !='' and (self.cleaned_data[field_name] !=getattr(self.instance, field_name) ):
                return self.check_field_value_unique(field_name=field_name)
            else:
                return getattr(self.instance, field_name)


    def clean_before(self):
        pass


    def clean_after(self):
        pass


    def clean(self):
        self.clean_before()
        for field in self.local_field_objects:
            if field.name != 'id' and hasattr(field, 'unique') and field.unique and hasattr(field, 'editable') and field.editable != False:
                self.cleaned_data[field.name] = self.check_field(field_name=field.name)
        self.clean_after()
        return self.cleaned_data


    def get_save_data(self, model=None):
        #print model
        field_objects = [ y[0] for y in model._meta.get_fields_with_model() ] #取得model中的全部field 对象

        save_dict = {}

        for field in field_objects:
            if self.instance != None:
                save_dict[field.name] = getattr(self.instance, field.name)

            if  hasattr(field, 'related') and field.name in self.fields.keys():  #判断是否为外键，然后取得该外键对象。 同时判断该field是否在本类中定义。
                pk_value = self.cleaned_data.get(field.name)
                try :
                    related_instance = field.related.parent_model.objects.get(pk=pk_value)
                    if related_instance:
                        save_dict[field.name] = related_instance
                except ValueError, e:
                    print "[Error] ValueError - Field(%s) : %s" % (field.name, e.message)
            elif hasattr(field, 'editable') and field.editable == True and field.name in self.fields.keys():  #判断此field是否可编辑！ 同时判断该field是否在本类中定义。
                field_value = self.cleaned_data.get(field.name)
                if field_value:
                    save_dict[field.name] = field_value

        return save_dict


    def as_table(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row='<tr%(html_class_attr)s><th>%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td></tr>',
            error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='</td></tr>',
            help_text_html='<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False)


    def as_ul(self):
        "Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._html_output(
            normal_row='<li%(html_class_attr)s>%(errors)s%(label)s %(field)s%(help_text)s</li>',
            error_row='<li>%s</li>',
            row_ender='</li>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=False)


    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)


    def as_bootstrap(self):
        "Returns this form rendered as HTML the bootstrap css style."
        return self._html_output(
            normal_row='''<div class="form-group">
                            <div class="col-sm-2 f1">%(label)s</div>
                            <div class="col-sm-4">%(field)s</div> %(errors)s
                          </div>''',
            error_row='<div class="col-sm-3 fe">%s</div>',
            row_ender='</div>',
            help_text_html='<div class="col-sm-1 fe">%s</div>',
            errors_on_separate_row=False)


    def save(self):
        #print "Get save data"
        save_args = self.get_save_data(self.model)
        #print "Save args : ",save_args
        for field in self.model._meta.fields:
            if  type(field) == models.DateTimeField and field.name in self.base_fields.keys() :
                try:
                    save_args[field.name] = datetime.strptime(save_args[field.name],'%Y/%m/%d')
                except ValueError,e:
                    try:
                        save_args[field.name] = datetime.strptime(save_args[field.name],'%Y-%m-%d')
                    except ValueError,e:
                        save_args[field.name] = datetime.strptime(save_args[field.name],'%Y-%m-%d %H:%M:%S')
                save_args[field.name] = save_args[field.name].strftime('%Y-%m-%d %H:%M:%S')


        field_objects =  self.model._meta.many_to_many
        if field_objects:
            for field in field_objects:
               save_args[field.name] = self.cleaned_data.get(field.name)

        new_instance = save_model_data(self.model,**save_args)
        return new_instance




class newChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), required=True, widget=None, label=None,
                 initial=None, help_text='',filter_status=None, *args, **kwargs):
        super(newChoiceField, self).__init__(choices=(), required=required, widget=widget, label=label,
                                        initial=initial, help_text=help_text, *args, **kwargs)

        self.filter_status = filter_status


