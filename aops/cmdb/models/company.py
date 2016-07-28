#coding=utf-8
from django.db import models
from django.core.urlresolvers import reverse

from aops.settings import INT_CHOICES, STATUS_CHOICES
from cmdb import signals

class Company(models.Model):
    name = models.CharField(max_length=255,unique=True)
    alias = models.CharField(max_length=255,unique=True)
    address =  models.CharField(max_length=255, null=True)
    mail = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'company'
        ordering = ['-name']
        app_label = 'cmdb'


    def __unicode__(self):
        return self.alias

 
    def search_name(self):
        return '%s:  %s # %s # %s' % (self.__class__.__name__, self.name, self.alias, self.address)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Company._meta.fields]

    def get_absolute_url(self):
        return reverse('cmdb:edit_company', args=[self.id])

    def delete(self, *args, **kwargs):
        super(Company, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.id is not None :
            supplier = Company.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(Company, self).save(*args, **kwargs)
