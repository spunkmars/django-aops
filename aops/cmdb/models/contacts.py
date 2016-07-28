#coding=utf-8
from django.db import models
from django.core.urlresolvers import reverse

from aops.settings import INT_CHOICES, STATUS_CHOICES
from cmdb import signals

from cmdb.models.company import Company

class Contacts(models.Model):
    name = models.CharField(max_length=255)
    job_titles = models.CharField(max_length=255)
    company = models.ForeignKey(Company)
    mail = models.CharField(max_length=255, null=True)
    im_num = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    mobile_phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    comment = models.CharField(max_length=255, null=True)
    status = models.IntegerField(editable=True, choices=STATUS_CHOICES, default=0)
    is_dynamic = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    is_deleted = models.IntegerField(editable=True, choices=INT_CHOICES, default=0)
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    update_time = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'contacts'
        ordering = ['-name']
        app_label = 'cmdb'



    def __unicode__(self):
        return "%s - %s - %s" % ( self.company.name, self.job_titles, self.name )

    def search_name(self):
        return '%s:  %s # %s # %s' % (self.__class__.__name__, self.company.name, self.job_titles, self.name)

    #为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in Contacts._meta.fields]

    def get_absolute_url(self):
        return reverse('cmdb:edit_contacts', args=[self.id])

    def delete(self, *args, **kwargs):
        #del member from group before del user
        #self.group.del_group_member(self.username)

        super(Contacts, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.id is not None :
            contacts = Contacts.objects.get(pk=self.id)

        else:
            print 'Alter'

        super(Contacts, self).save(*args, **kwargs)



