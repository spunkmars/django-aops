#coding=utf-8

from datetime import datetime

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

from aops.settings import INT_CHOICES, STATUS_CHOICES, NETWORKING_HARDWARE_TYPE_CHOICES
from cmdb import signals
from cmdb.models.contract import Contract
from cmdb.models.ip_record import IpRecord
from cmdb.models.brand import Brand
from cmdb.models.company import Company

class NetworkEquipment(models.Model):
    uuid = models.CharField(max_length=255, unique=True)
    ip_record = models.ManyToManyField(IpRecord, related_name='network_equipment_ip_record', null=True)
    manufacturer =  models.ForeignKey(Company, null=True)
    brand = models.ForeignKey(Brand, null=True)
    model_num = models.CharField(max_length=255)
    serial = models.CharField(max_length=255, unique=True)
    idc_device_num = models.CharField(max_length=255)
    volume = models.IntegerField(max_length=4)
    asset_num = models.CharField(max_length=255, null=True)
    order_num = models.CharField(max_length=255, null=True)
    order_date = models.DateTimeField(null=True)
    price = models.IntegerField(max_length=10, null=True)
    equipment_type = models.CharField(max_length=45, editable=True, choices=NETWORKING_HARDWARE_TYPE_CHOICES, default='switch')
    total_ports = models.IntegerField(max_length=10, null=True)
    warranty_period = models.DateTimeField( null=True)
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_remote_control = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_run = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'network_equipment'
        ordering = ['-uuid']
        app_label = 'cmdb'

    def __unicode__(self):
        return self.uuid

    def search_name(self):
        return '%s:  %s # %s # %s # %s' % (self.__class__.__name__, self.manufacturer.name, self.brand.name, self.model_num, self.uuid )

    def get_absolute_url(self):
        return reverse('cmdb:edit_network_equipment', args=[self.id])

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in NetworkEquipment._meta.fields]

    def delete(self, *args, **kwargs):
        super(NetworkEquipment, self).delete(*args, **kwargs)


    def save(self, *args, **kwargs):

        if self.id is not None :
            network_equipment = NetworkEquipment.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(NetworkEquipment, self).save(*args, **kwargs)
