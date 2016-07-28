#coding=utf-8
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _

from libs.forms.common import newModelForm, newChoiceField, EXPIRATION_YEAR_CHOICES
from libs.forms.field import newDateTimeInput

class DomainNameForm(newModelForm):
    contract = newChoiceField(choices=(),  label=_('Contract'), widget=forms.Select(attrs={'class':'form-control'}))
    name = forms.CharField(max_length=255, label=_('Name'), widget=forms.TextInput(attrs={'class':'form-control'}))
    application_date = forms.CharField(max_length=255, label=_('Application Date'), required=False, widget=newDateTimeInput(d_type='onlydate', attrs={'class':'form-control'}))
    deadline = forms.CharField(max_length=255, label=_('Deadline'), required=False, widget=newDateTimeInput(d_type='onlydate', attrs={'class':'form-control'}))
    resolution_supplier=  newChoiceField(choices=(), label=_('Resolution Supplier'), widget=forms.Select(attrs={'class':'form-control'}))
    supplier = newChoiceField(choices=(),  label= _('Supplier'), widget=forms.Select(attrs={'class':'form-control'}))
    dns_server = forms.CharField(max_length=255, label=_('Dns Server'), required=False,  widget=forms.TextInput(attrs={'class':'form-control'}))
    status = newChoiceField(choices=(), label=_('Status'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    comment = forms.CharField(max_length=255, label=_('Comment'), required=False,  widget=forms.TextInput(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'),required=False,  widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.Select(attrs={'class':'form-control'}))

    
    

