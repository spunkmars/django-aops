#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from libs.forms.common import newModelForm, newChoiceField


class DeviceForm(newModelForm):
    contract = newChoiceField(choices=(),  label=_('Contract'), widget=forms.Select(attrs={'class':'form-control'}))
    cabinet_seat = newChoiceField(choices=(), label=_('Cabinet Seat'),  widget=forms.Select(attrs={'class':'form-control'}), filter_status=0)
    type = forms.CharField(max_length=255, label=_('Type'), widget=forms.HiddenInput())
    device_id = forms.CharField(max_length=255, label=_('Device ID'), widget=forms.HiddenInput())
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.HiddenInput())
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.HiddenInput())