#coding=utf-8
from django.db import models

from aops.settings import INT_CHOICES, STATUS_CHOICES, DOMAIN_RECORD_TYPE_CHOICES
from cmdb import signals
from cmdb.models.domain_name import DomainName
from cmdb.models.ip_record import IpRecord
class DomainRecord(models.Model):
    domain_name = models.ForeignKey(DomainName, related_name='domain_name_record')
    ip_record = models.ManyToManyField(IpRecord, related_name='domain_ip_record', null=True)
    record_value = models.CharField(max_length=45, null=True)
    record_type = models.IntegerField(editable=True, choices=DOMAIN_RECORD_TYPE_CHOICES, default=0)
    host_name = models.CharField(max_length=45)
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)


    class Meta:
        db_table = 'domain_record'
        ordering = ['-domain_name']
        app_label = 'cmdb'
        unique_together = (("domain_name","host_name"))

    def __unicode__(self):
        return '%s.%s' % (self.host_name, self.domain_name)

    def search_name(self):        
        return '%s:  %s # %s # %s' % (self.__class__.__name__, self.domain_name.name, self.record_type, self.host_name)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in DomainRecord._meta.fields]


    def delete(self, *args, **kwargs):
        super(DomainRecord, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.id is not None :
            domain_record = DomainRecord.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(DomainRecord, self).save(*args, **kwargs)
