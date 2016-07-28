#coding=utf-8

from django.db import models
from django.core.urlresolvers import reverse

from aops.settings import INT_CHOICES, STATUS_CHOICES, CONTRACT_CHOICES
from cmdb import signals
from cmdb.models.contacts import Contacts
from cmdb.models.company import Company

class Contract(models.Model):
    contract_serial = models.CharField(max_length=255, unique=True)
    contract_name = models.CharField(max_length=255)
    contract_type = models.IntegerField(editable=True, choices=CONTRACT_CHOICES, default=0)
    contract_outline = models.CharField(max_length=1800,default='')
    company = models.ForeignKey(Company)
    signing_time = models.DateTimeField(blank=True)
    deadline = models.DateTimeField(blank=True)
    signers_contacts = models.ForeignKey(Contacts, related_name="contract_signers_contacts")
    supplier_contacts = models.ForeignKey(Contacts, related_name="contract_supplier_contacts")
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'contract'
        ordering = ['-contract_name']
        app_label = 'cmdb'

    def __unicode__(self):
        return self.contract_name

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Contract._meta.fields]

    def get_absolute_url(self):
        return reverse('cmdb:edit_contract', args=[self.id])

    def delete(self, *args, **kwargs):
        super(Contract, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.id is not None :
            contract = Contract.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(Contract, self).save(*args, **kwargs)
