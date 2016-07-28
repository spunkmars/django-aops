#coding=utf-8

from datetime import datetime

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

from aops.settings import INT_CHOICES, STATUS_CHOICES
from cmdb import signals
from cmdb.models.ip_record import IpRecord
from cmdb.models.physical_server import PhysicalServer

class Host(models.Model):
    uuid = models.CharField(max_length=255,unique=True)
    roles = models.CharField(max_length=255, null=True)
    physical_server = models.ForeignKey(PhysicalServer, related_name='host_physical_server', null=True)
    salt_id =  models.CharField(max_length=255, null=True)
    ip_record = models.ManyToManyField(IpRecord, related_name='host_ip_record', null=True)
    operating_system = models.CharField(max_length=255, null=True)
    os_version = models.CharField(max_length=255, null=True)
    host_name = models.CharField(max_length=255, null=True)
    processor = models.CharField(max_length=255, null=True)
    memory = models.CharField(max_length=255, null=True)
    harddisk = models.CharField(max_length=255, null=True)
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_run = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_virtual_machine = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'host'
        ordering = ['-uuid']
        app_label = 'cmdb'

    def __unicode__(self):
        return self.uuid

    def search_name(self):
        return '%s:  %s # %s # %s # %s # %s # %s # %s' % (self.__class__.__name__, self.uuid, self.roles, self.physical_server.__unicode__(), self.salt_id, self.operating_system, self.os_version, self.host_name)

    def get_absolute_url(self):
        return reverse('cmdb:edit_host', args=[self.id])

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Host._meta.fields]

    def delete(self, *args, **kwargs):
        super(Host, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.id is not None :
            host = Host.objects.get(pk=self.id)
        else:
            print 'Alter'
        super(Host, self).save(*args, **kwargs)
