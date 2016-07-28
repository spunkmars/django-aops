#coding=utf-8
from django.db import models
from django.core.urlresolvers import reverse

from aops.settings import INT_CHOICES, STATUS_CHOICES
from cmdb import signals
from cmdb.models.idc_contract import IdcContract

class Cabinet(models.Model):
    idc_contract = models.ForeignKey(IdcContract)
    cabinet_name = models.CharField(max_length=255)
    cabinet_location = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cabinet'
        ordering = ['-cabinet_name']
        app_label = 'cmdb'
        unique_together = (("cabinet_name","cabinet_location"),)

    def __unicode__(self):
        return '%s-%s' % (self.idc_contract.idc.idc_name, self.cabinet_name)

    def search_name(self):
        return '%s:  %s # %s' % (self.__class__.__name__, self.cabinet_name, self.cabinet_location)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Cabinet._meta.fields]

    def get_absolute_url(self):
        return reverse('cmdb:edit_cabinet', args=[self.id])

    def delete(self, *args, **kwargs):
        super(Cabinet, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.id is not None :
            cabinet = Cabinet.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(Cabinet, self).save(*args, **kwargs)
