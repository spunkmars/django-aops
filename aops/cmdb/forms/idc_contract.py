#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from libs.forms.common import newModelForm, newChoiceField


class IdcContractForm(newModelForm):
    idc = newChoiceField(choices=(),  label=_('IDC'), widget=forms.Select(attrs={'class':'form-control'}))
    contract = newChoiceField(choices=(),  label=_('Contract'), widget=forms.Select(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.Select(attrs={'class':'form-control'}))


