#coding=utf-8
from django.db import models

from aops.settings import INT_CHOICES, STATUS_CHOICES, IP_PURPOSE_CHOICES
from cmdb import signals
from cmdb.models.ip_resource import IpResource

class IpRecord(models.Model):
    ip_resource = models.ForeignKey(IpResource, related_name='ip_resource_record')
    purpose = models.IntegerField(editable=True, choices=IP_PURPOSE_CHOICES, default=0)
    alias = models.CharField(max_length=255, unique=True)
    ip_address = models.CharField(max_length=45)
    mask = models.CharField(max_length=45)
    gateway = models.CharField(max_length=45, null=True)
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    '''
       待定字段
      `bind_object_type` VARCHAR(255) NULL DEFAULT NULL COMMENT ' 绑定类型',
      `bind_object_value` INT(10)  NULL DEFAULT NULL COMMENT '绑定类型值',
    '''

    class Meta:
        db_table = 'ip_record'
        ordering = ['-ip_address']
        app_label = 'cmdb'
        unique_together = (("ip_resource","ip_address"),)

    def __unicode__(self):
        return "%s(%s)" %( self.ip_address, self.alias)

    def search_name(self):                
        return '%s:  %s # %s # %s # %s' % (self.__class__.__name__, self.ip_resource.__unicode__(), self.alias,self.ip_address, self.mask)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in IpRecord._meta.fields]


    def delete(self, *args, **kwargs):
        super(IpRecord, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.id is not None :
            ip_record = IpRecord.objects.get(pk=self.id)

        else:
            print 'Alter'
        super(IpRecord, self).save(*args, **kwargs)
