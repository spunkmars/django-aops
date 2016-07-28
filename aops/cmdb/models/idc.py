#coding=utf-8

from datetime import datetime

from django.db import models
from django.utils import timezone

from aops.settings import INT_CHOICES, STATUS_CHOICES
from cmdb import signals

from cmdb.models.contract import Contract
from cmdb.models.company import Company

class Idc(models.Model):
    contract = models.ManyToManyField(Contract, through='IdcContract')
    idc_name = models.CharField(max_length=255, unique=True)
    idc_address = models.CharField(max_length=255)
    company = models.ForeignKey(Company)
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'idc'
        ordering = ['-idc_name']
        app_label = 'cmdb'

    def __unicode__(self):
        return '%s(%s)' % (self.idc_name, self.company)

    def search_name(self):        
        return '%s:  %s # %s # %s' % (self.__class__.__name__, self.idc_name, self.idc_address, self.company.name)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Idc._meta.fields]

    def delete(self, *args, **kwargs):
        super(Idc, self).delete(*args, **kwargs)


    def save(self, *args, **kwargs):
        if self.id is not None :
            idc = Idc.objects.get(pk=self.id)
        else:
            print 'Alter'
        super(Idc, self).save(*args, **kwargs)
