#coding=utf-8

from datetime import datetime

from django.db import models
from django.utils import timezone

from aops.settings import INT_CHOICES, STATUS_CHOICES
from cmdb import signals
from cmdb.models.contract import Contract
from cmdb.models.domain_record import DomainRecord
from cmdb.models.company import Company

class Cdn(models.Model):
    company = models.ForeignKey(Company)
    contract = models.ForeignKey(Contract)
    domain_record = models.ManyToManyField(DomainRecord, through='CdnDomainRecord')
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cdn'
        ordering = ['-company']
        app_label = 'cmdb'
        unique_together = (("company","contract"),)

    def __unicode__(self):
        return self.company

    def search_name(self):
        return '%s:  %s # %s' % (self.__class__.__name__, self.company, self.contract.name)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Cdn._meta.fields]

    def delete(self, *args, **kwargs):
        #del member from group before del user
        #self.group.del_group_member(self.username)
        #signals.delete_cdn_done.send(sender=Cdn, obj=self)
        super(Cdn, self).delete(*args, **kwargs)

#    def pre_save(self, model_instance, add):
#        if self.auto_now or (self.auto_now_add and add):
#            #value = datetime.date.today()
#            #value = datetime.now().replace(tzinfo=timezone.utc)
#            value = timezone.now().date()
#            setattr(model_instance, self.attname, value)
#            return value
#        else:
#            return super(DateField, self).pre_save(model_instance, add)

    def save(self, *args, **kwargs):

        if self.id is not None :
            cdn = Cdn.objects.get(pk=self.id)

        else:
            print 'geng gai'

        super(Cdn, self).save(*args, **kwargs)
