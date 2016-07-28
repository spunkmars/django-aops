#coding=utf-8
from django.db import models
from django.core.urlresolvers import reverse

from aops.settings import INT_CHOICES, STATUS_CHOICES, OPERATOR_CHOICES, IP_PURPOSE_CHOICES
from cmdb import signals
from cmdb.models.idc_contract import IdcContract


class IpResource(models.Model):
    idc_contract = models.ForeignKey(IdcContract)
    purpose = models.IntegerField(editable=True, choices=IP_PURPOSE_CHOICES, default=0)
    alias = models.CharField(max_length=255, unique=True)
    begin_ip = models.CharField(max_length=45)
    end_ip = models.CharField(max_length=45)
    mask = models.CharField(max_length=45)
    gateway = models.CharField(max_length=45)
    dns = models.CharField(max_length=45, null=True)
    operator = models.CharField(max_length=45, editable=True, choices=OPERATOR_CHOICES, default='lan')
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)


    class Meta:
        db_table = 'ip_resource'
        ordering = ['-begin_ip']
        app_label = 'cmdb'
        unique_together = (("idc_contract", "begin_ip", "end_ip"),)

    def __unicode__(self):
        return "%s : %s ~ %s" % (self.alias, self.begin_ip, self.end_ip)

    def search_name(self):                       
        return '%s:  %s # %s # %s # %s # %s # %s # %s' % (self.__class__.__name__,  self.alias, self.begin_ip, self.end_ip, self.mask, self.gateway, self.dns, self.operator)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in IpResource._meta.fields]

    def get_absolute_url(self):
        return reverse('cmdb:edit_ip_resource', args=[self.id])

    def delete(self, *args, **kwargs):
        super(IpResource, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.id is not None :
            ip_resource = IpResource.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(IpResource, self).save(*args, **kwargs)
