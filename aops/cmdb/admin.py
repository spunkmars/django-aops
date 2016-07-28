from django.contrib import admin

# Register your models here.

from cmdb.models.contacts import Contacts
from cmdb.models.contract import Contract
from cmdb.models.cdn import Cdn

admin.site.register(Contacts)
admin.site.register(Contract)
admin.site.register(Cdn)
