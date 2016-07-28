#coding=utf-8
from django.db import models

from aops.settings import INT_CHOICES
from cmdb import signals
from cmdb.models.idc import Idc
from cmdb.models.contract import Contract
from django.db import IntegrityError

class IdcContract(models.Model):
    idc = models.ForeignKey(Idc)
    contract = models.ForeignKey(Contract)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    update_time = models.DateTimeField(blank=True, null=True, auto_now=True)


    class Meta:
        db_table = 'idc_contract'
        ordering = ['-id']
        app_label = 'cmdb'
        unique_together = (("idc","contract"),)

    def __unicode__(self):
        return u"%s - %s" % (self.idc ,self.contract)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in IdcContract._meta.fields]


    def delete(self, *args, **kwargs):
        super(IdcContract, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.id is not None :
            r_idc_contract = IdcContract.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(IdcContract, self).save(*args, **kwargs)



