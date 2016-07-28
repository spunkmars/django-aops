#coding=utf-8

from datetime import datetime

from django.db import models
from django.utils import timezone

from aops.settings import INT_CHOICES
from cmdb import signals
from cmdb.models.contract import Contract
from cmdb.models.cabinet_seat import CabinetSeat

class Device(models.Model):
    contract = models.ForeignKey(Contract)
    cabinet_seat = models.ForeignKey(CabinetSeat)
    type = models.CharField(max_length=45)
    device_id = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, null=True)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'device'
        ordering = ['-device_id']
        app_label = 'cmdb'
        unique_together = (("contract","cabinet_seat"),("type","device_id"))

    def __unicode__(self):
        return "%s - %s - %s - %s" % (self.contract, self.cabinet_seat, self.type, self.device_id)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Device._meta.fields]

    def delete(self, *args, **kwargs):
        super(Device, self).delete(*args, **kwargs)


    def save(self, *args, **kwargs):

        if self.id is not None :
            idc = Device.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(Device, self).save(*args, **kwargs)
