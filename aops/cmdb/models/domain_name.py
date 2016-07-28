#coding=utf-8
from django.db import models
from django.core.urlresolvers import reverse

from aops.settings import INT_CHOICES, STATUS_CHOICES
from cmdb import signals
from cmdb.models.contract import Contract
from cmdb.models.company import Company

class DomainName(models.Model):
    contract = models.ForeignKey(Contract)
    name = models.CharField(max_length=45,unique=True)
    application_date = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    resolution_supplier = models.ForeignKey(Company, related_name="dn_res_supplier")
    supplier = models.ForeignKey(Company, related_name="dn_supplier")
    dns_server = models.CharField(max_length=45, null=True)
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'domain_name'
        ordering = ['-name']
        app_label = 'cmdb'
        unique_together = (("contract","name"))

    def __unicode__(self):
        return self.name

    def search_name(self):
        return '%s:  %s # %s # %s # %s # %s # %s' % (self.__class__.__name__, self.name, self.application_date, self.deadline, self.resolution_supplier, self.supplier, self.dns_server)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in DomainName._meta.fields]

    def get_absolute_url(self):
        return reverse('cmdb:edit_domain_name', args=[self.id])

    def delete(self, *args, **kwargs):
        super(DomainName, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.id is not None :
            domain_name = DomainName.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(DomainName, self).save(*args, **kwargs)
