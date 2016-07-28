#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from libs.forms.common import newModelForm, newChoiceField


class IpRecordForm(newModelForm):
    ip_resource = newChoiceField(choices=(),  label=_('IP Resource'), widget=forms.Select(attrs={'class':'form-control'}))
    alias = forms.CharField(max_length=255, label=_('Alias'), widget=forms.TextInput(attrs={'class':'form-control'}))
    purpose = newChoiceField(choices=(), label=_('Purpose'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    ip_address = forms.CharField(max_length=255, label=_('IP address'), widget=forms.TextInput(attrs={'class':'form-control'}))
    mask = forms.CharField(max_length=255, label=_('Mask'), widget=forms.TextInput(attrs={'class':'form-control'}))
    gateway = forms.CharField(max_length=255, label=_('Gateway'),required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    status = newChoiceField(choices=(), label=_('Status'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    comment = forms.CharField(max_length=255, label=_('Comment'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
