#coding=utf-8

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from libs.forms.common import EXPIRATION_YEAR_CHOICES
from libs.forms.field import newDateTimeInput
from libs.forms.common import newModelForm, newChoiceField


class ContractForm(newModelForm):
    contract_serial = forms.CharField(max_length=255, label=string_concat(_('Contract')," ", _('serial')), widget=forms.TextInput(attrs={'class':'form-control'}))
    contract_name = forms.CharField(max_length=255, label=string_concat(_('Contract')," ", _('name')), widget=forms.TextInput(attrs={'class':'form-control'}))
    contract_type = newChoiceField(choices=(), label=string_concat(_('Contract')," ", _('type')),widget=forms.Select(attrs={'class':'form-control'}))
    contract_outline = forms.CharField(max_length=1800, label=string_concat(_('Contract')," ", _('outline')),widget=forms.Textarea(attrs={'class':'form-control'}))
    company = newChoiceField(choices=(),  label= _('Supplier'), widget=forms.Select(attrs={'class':'form-control'}))
    signing_time =  forms.CharField(max_length=255, label=_('Signing time'), required=False, widget=newDateTimeInput(d_type='onlydate', attrs={'class':'form-control'}))
    deadline = forms.CharField(max_length=255, label=_('Deadline'), required=False, widget=newDateTimeInput(d_type='onlydate', attrs={'class':'form-control'}))
    signers_contacts = newChoiceField(choices=(),  label=string_concat(_('Signers'),' ', _('contacts')), widget=forms.Select(attrs={'class':'form-control'}))
    supplier_contacts = newChoiceField(choices=(),  label=string_concat(_('Supplier'),' ', _('contacts')), widget=forms.Select(attrs={'class':'form-control'}))
    status = newChoiceField(choices=(), label=_('Status'), widget=forms.Select(attrs={'class':'form-control'}))
    comment = forms.CharField(max_length=255, label=_('Comment'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.Select(attrs={'class':'form-control'}))


