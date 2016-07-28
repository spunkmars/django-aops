#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from libs.forms.common import newModelForm, newChoiceField


class IpResourceForm(newModelForm):
    idc_contract = newChoiceField(choices=(),  label=_('Idc Contract'), widget=forms.Select(attrs={'class':'form-control'}))
    alias = forms.CharField(max_length=45,  label=_('Alias'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    purpose = newChoiceField(choices=(), label=_('Purpose'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    operator = newChoiceField(choices=(), label=_('Operator'),  widget=forms.Select(attrs={'class':'form-control'}))
    begin_ip = forms.CharField(max_length=255, label=_('Begin IP'), widget=forms.TextInput(attrs={'class':'form-control'}))
    end_ip = forms.CharField(max_length=255, label=_('End IP'), widget=forms.TextInput(attrs={'class':'form-control'}))
    mask = forms.CharField(max_length=255, label=_('Mask'), widget=forms.TextInput(attrs={'class':'form-control'}))
    gateway = forms.CharField(max_length=255, label=_('Gateway'), widget=forms.TextInput(attrs={'class':'form-control'}))
    dns =  forms.CharField(max_length=255, label=_('Dns'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    comment =  forms.CharField(max_length=255, label=_('Comment'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    status = newChoiceField(choices=(), label=_('Status'), required=False, widget=forms.Select(attrs={'class':'form-control'}))




