#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from libs.forms.common import newModelForm, newChoiceField


class CabinetSeatForm(newModelForm):
    cabinet = newChoiceField(choices=(),  label=_('Cabinet'), widget=forms.Select(attrs={'class':'form-control'}))
    cabinet_seat_location = forms.CharField(max_length=255, label=_('Cabinet Seat location'), widget=forms.TextInput(attrs={'class':'form-control'}))
    status = newChoiceField(choices=(), label=_('Status'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    comment = forms.CharField(max_length=255, label=_('Comment'), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_dynamic = newChoiceField(choices=(), label=_('Is dynamic'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
    is_deleted = newChoiceField(choices=(), label=_('Is deleted'), required=False, widget=forms.Select(attrs={'class':'form-control'}))
