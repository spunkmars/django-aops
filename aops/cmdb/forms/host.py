#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from libs.forms.field import AutoGetVal
from libs.forms.common import newModelForm, newChoiceField
from cmdb.models.ip_record import IpRecord


class HostForm(newModelForm):
    physical_server = newChoiceField(choices=(),  label=_('Pyhsical server'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    uuid = forms.CharField(max_length=255, label=_('UUID'), widget=AutoGetVal(g_url='cmdb:get_uuid', d_type='cmdb.uuid',attrs={'class':'form-control'}))
    salt_id = forms.CharField(max_length=255, label=_('SaltID'), required=False, widget=AutoGetVal(g_url='cmdb:get_salt_id', d_type='cmdb.saltid',attrs={'class':'form-control'}))
    ip_record = forms.ModelMultipleChoiceField( queryset=IpRecord.objects.filter(status=1).order_by('id'),label=_('IP'), required=False,  widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    operating_system =forms.CharField(max_length=255, label=_('Operating system'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    os_version = forms.CharField(max_length=255, label=_('OS version'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    host_name = forms.CharField(max_length=255, label=_('Host name'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    processor = forms.CharField(max_length=255, label=_('Processor'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    memory = forms.CharField(max_length=255, label=_('Memory'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    harddisk = forms.CharField(max_length=255, label=_('Harddisk'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    roles = forms.CharField(max_length=255, label=_('Roles'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    status = newChoiceField(choices=(), label=_('Status'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    comment = forms.CharField(max_length=255, label=_('Comment'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_run = newChoiceField(choices=(), label=_('Is run'), required=False,  widget=forms.Select(attrs={'class':'form-control'}))
    is_virtual_machine = newChoiceField(choices=(), label=_('Is virtual machine'), required=False,  widget=forms.Select(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False,  widget=forms.Select(attrs={'class':'form-control'}))



