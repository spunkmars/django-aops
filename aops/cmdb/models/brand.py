#coding=utf-8
from django.db import models
from django.core.urlresolvers import reverse

from aops.settings import INT_CHOICES, STATUS_CHOICES
from cmdb import signals

from cmdb.models.company import Company

class Brand(models.Model):
    name = models.CharField(max_length=45, unique=True)
    company = models.ForeignKey(Company, null=True)
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'brand'
        ordering = ['-name']
        app_label = 'cmdb'

    def __unicode__(self):
        return self.name

    def search_name(self):
        return '%s:  %s # %s' % (self.__class__.__name__, self.name, self.company)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Brand._meta.fields]

    def get_absolute_url(self):
        return reverse('cmdb:edit_brand', args=[self.id])

    def delete(self, *args, **kwargs):
        super(Brand, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.id is not None :
            brand = Brand.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(Brand, self).save(*args, **kwargs)
