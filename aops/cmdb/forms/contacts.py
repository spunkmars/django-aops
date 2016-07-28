#coding=utf-8


from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from libs.forms.common import newModelForm, newChoiceField


class ContactsForm(newModelForm):
    name = forms.CharField(max_length=255, label=string_concat(_('Contact')," ", _('name')), widget=forms.TextInput(attrs={'class':'form-control'}))
    job_titles = forms.CharField(max_length=255, label=_('Job titles'), widget=forms.TextInput(attrs={'class':'form-control'}))
    company =  newChoiceField(choices=(),  label= _('Company'), widget=forms.Select(attrs={'class':'form-control'}))
    mail = forms.EmailField(max_length=255, label=_('Email'), required=False, widget=forms.EmailInput(attrs={'class':'form-control'}))
    im_num = forms.CharField(max_length=255, label=_('IM'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone =  forms.CharField(max_length=255, label=_('Phone'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    mobile_phone = forms.CharField(max_length=255, label=_('Mobile phone'), widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(max_length=255, label=_('Address'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    comment = forms.CharField(max_length=255, label=_('Comment'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))


