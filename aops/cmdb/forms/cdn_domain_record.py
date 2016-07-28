#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from libs.forms.common import newModelForm, newChoiceField


class CdnDomainRecordForm(newModelForm):
    cdn = newChoiceField(choices=(),  label=_('CDN'), widget=forms.Select(attrs={'class':'form-control'}))
    domain_record = newChoiceField(choices=(),  label=_('Domain Record'), widget=forms.Select(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
