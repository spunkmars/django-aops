#coding=utf-8
from django.db import models

from aops.settings import INT_CHOICES, STATUS_CHOICES
from cmdb import signals
from cmdb.models.cdn import Cdn
from cmdb.models.domain_record import DomainRecord


class CdnDomainRecord(models.Model):
    cdn = models.ForeignKey(Cdn)
    domain_record = models.ForeignKey(DomainRecord)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'cdn_domain_record'
        ordering = ['-id']
        app_label = 'cmdb'
        unique_together = (("cdn","domain_record"),)

    def __unicode__(self):
        return self.id

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in CdnDomainRecord._meta.fields]


    def delete(self, *args, **kwargs):
        super(CdnDomainRecord, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.id is not None :
            r_cdn_domain_record = CdnDomainRecord.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(CdnDomainRecord, self).save(*args, **kwargs)
