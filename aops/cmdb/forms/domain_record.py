#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from libs.forms.common import newModelForm, newChoiceField
from cmdb.models.ip_record import  IpRecord


class DomainRecordForm(newModelForm):
    domain_name  = newChoiceField(choices=(),  label=_('Domain name'), widget=forms.Select(attrs={'class':'form-control'}))
    ip_record = forms.ModelMultipleChoiceField( queryset=IpRecord.objects.order_by('id'),label=_('IP'),
                                                widget=forms.SelectMultiple(attrs={'class':'form-control'}),required=False)
    record_type = forms.ChoiceField(choices=(), label=_('Record Type'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    record_value = forms.CharField(max_length=255, label=_('Record Value'),required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    host_name = forms.CharField(max_length=255, label=_('Host Name'),required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    status = newChoiceField(choices=(), label=_('Status'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    comment = forms.CharField(max_length=255, label=_('Comment'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.Select(attrs={'class':'form-control'}))

