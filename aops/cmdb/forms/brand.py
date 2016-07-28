#coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

from libs.forms.common import newModelForm, newChoiceField


class BrandForm(newModelForm):
    name = forms.CharField(max_length=255, label= _('Name'), widget=forms.TextInput(attrs={'class':'form-control'}))
    company = newChoiceField(choices=(), label=_('Company'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    comment = forms.CharField(max_length=255, label=_('Comment'), required=False,  widget=forms.TextInput(attrs={'class':'form-control'}))
    status = newChoiceField(choices=(), label=_('Status'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
