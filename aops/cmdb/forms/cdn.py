#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from libs.forms.common import newModelForm,newChoiceField
from cmdb.models.domain_record import  DomainRecord


class CdnForm(newModelForm):
    company = newChoiceField(choices=(),  label= _('Supplier'), widget=forms.Select(attrs={'class':'form-control'}))
    contract = newChoiceField(choices=(),  label=string_concat(_('Contract'),' ', _('ID')), widget=forms.Select(attrs={'class':'form-control'}))
    domain_record = forms.ModelMultipleChoiceField( queryset=DomainRecord.objects.order_by('id'),label=_('Domain Record'), widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    comment = forms.CharField(max_length=255, label=string_concat(_('Supplier'),' ', _('Comment')), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    status = newChoiceField(choices=(), label=_('Status'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.Select(attrs={'class':'form-control'}))