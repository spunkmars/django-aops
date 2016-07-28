#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from libs.forms.common import newModelForm, newChoiceField
from cmdb.models.contract import Contract


class IdcForm(newModelForm):
    contract = forms.ModelMultipleChoiceField( queryset=Contract.objects.order_by('id'),label=_('Contract'), widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    idc_name = forms.CharField(max_length=255, label=string_concat(_('IDC'), ' ', _('Name')), widget=forms.TextInput(attrs={'class':'form-control'}))
    idc_address = forms.CharField(max_length=255, label=string_concat(_('IDC'), ' ', _('Address')), widget=forms.TextInput(attrs={'class':'form-control'}))
    company = newChoiceField(choices=(),  label= _('Company'), widget=forms.Select(attrs={'class':'form-control'}))
    status = newChoiceField(choices=(), label=_('Status'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    comment = forms.CharField(max_length=255, label=_('Comment'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
