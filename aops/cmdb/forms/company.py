#coding=utf-8


from django import forms
from django.utils.translation import ugettext_lazy as _

from libs.forms.common import newModelForm, newChoiceField


class CompanyForm(newModelForm):
    name = forms.CharField(max_length=255, label= _('Name'), widget=forms.TextInput(attrs={'class':'form-control'}))
    alias = forms.CharField(max_length=255, label= _('Alias'), widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(max_length=255, label=_('Address'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    mail = forms.EmailField(max_length=255, label=_('Email'), required=False, widget=forms.EmailInput(attrs={'class':'form-control'}))
    phone =  forms.CharField(max_length=255, label=_('Phone'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    comment = forms.CharField(max_length=255, label=_('Comment'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    status = newChoiceField(choices=(), label=_('Status'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.Select(attrs={'class':'form-control'}))


