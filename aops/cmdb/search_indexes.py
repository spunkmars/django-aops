from haystack import indexes
from cmdb.models.device import Device
from cmdb.models.idc_contract import IdcContract
from cmdb.models.cdn import Cdn
from cmdb.models.brand import Brand
from cmdb.models.cabinet import Cabinet
from cmdb.models.cabinet_seat import CabinetSeat
from cmdb.models.cdn_domain_record import CdnDomainRecord
from cmdb.models.company import Company
from cmdb.models.contacts import Contacts
from cmdb.models.contract import Contract
from cmdb.models.domain_name import DomainName
from cmdb.models.domain_record import DomainRecord
from cmdb.models.host import Host
from cmdb.models.idc import Idc
from cmdb.models.ip_record import IpRecord
from cmdb.models.ip_resource import IpResource
from cmdb.models.network_equipment import NetworkEquipment
from cmdb.models.physical_server import PhysicalServer

#class CompanyIndex(indexes.SearchIndex, indexes.Indexable):
#    text = indexes.CharField(document=True, use_template=True)
#    name = indexes.CharField(model_attr='name')
#    address = indexes.CharField(model_attr='address')
#
#    def get_model(self):
#        return Company
#
#    def index_queryset(self, using=None):
#        return self.get_model().objects.all()

class CompanyIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Company
        fields = ['name', 'alias', 'address', 'phone', 'email', 'comment']

class DeviceIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Device
        fields = ['cabinet_seat', u'cabinet_seat_id', 'comment', 'contract', u'contract_id', 'create_time', 'device_id', u'id', 'is_deleted', 'is_dynamic', 'type', 'update_time']

class IdcContractIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = IdcContract
        fields = ['cabinet', 'contract', u'contract_id', 'create_time', u'id', 'idc', u'idc_id', 'ipresource', 'is_deleted', 'is_dynamic', 'update_time']

class CdnIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Cdn
        fields = ['comment', 'company', 'create_time', 'is_deleted', 'is_dynamic', 'status', 'update_time']

class BrandIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Brand
        fields = ['comment', 'company', u'company_id', 'create_time', u'id', 'is_deleted', 'is_dynamic', 'name', 'networkequipment', 'physicalserver', 'status', 'update_time']

class CabinetIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Cabinet
        fields = ['cabinet_location', 'cabinet_name', 'cabinetseat', 'comment', 'create_time', u'id', 'idc_contract', u'idc_contract_id', 'is_deleted', 'is_dynamic', 'status', 'update_time']

class CabinetSeatIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = CabinetSeat
        fields = ['cabinet', u'cabinet_id', 'cabinet_seat_location', 'comment', 'create_time', 'device', u'id', 'is_deleted', 'is_dynamic', 'status', 'update_time']

#class CdnDomainRecordIndex(indexes.ModelSearchIndex, indexes.Indexable):
#    class Meta:
#        model = CdnDomainRecord
#        fields = ['cdn', 'create_time', 'is_deleted', 'is_dynamic', 'update_time']

class CompanyIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Company
        fields = ['address', 'alias', 'brand', 'cdn', 'comment', 'contacts', 'contract', 'create_time', u'dn_res_supplier', u'dn_supplier', u'id', 'idc', 'is_deleted', 'is_dynamic', 'mail', 'name', 'networkequipment', 'phone', 'physicalserver', 'status', 'update_time']

class ContactsIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Contacts
        fields = ['address', 'comment', 'company', u'company_id', u'contract_signers_contacts', u'contract_supplier_contacts', 'create_time', u'id', 'im_num', 'is_deleted', 'is_dynamic', 'job_titles', 'mail', 'mobile_phone', 'name', 'phone', 'status', 'update_time']

class ContractIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Contract
        fields = ['cdn', 'comment', 'company', u'company_id', 'contract_name', 'contract_outline', 'contract_serial', 'contract_type', 'create_time', 'deadline', 'device', 'domainname', u'id', 'idc', 'idccontract', 'is_deleted', 'is_dynamic', 'signers_contacts', u'signers_contacts_id', 'signing_time', 'status', 'supplier_contacts', u'supplier_contacts_id', 'update_time']

class DomainNameIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = DomainName
        fields = ['application_date', 'comment', 'contract', u'contract_id', 'create_time', 'deadline', 'dns_server', u'domain_name_record', u'id', 'is_deleted', 'is_dynamic', 'name', 'resolution_supplier', u'resolution_supplier_id', 'status', 'supplier', u'supplier_id', 'update_time']

class DomainRecordIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = DomainRecord
        fields = ['cdn', 'comment', 'create_time', 'domain_name', 'host_name', 'is_deleted', 'is_dynamic', 'record_type', 'status', 'update_time']

class HostIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Host
        fields = ['comment', 'create_time', 'harddisk',  'is_deleted', 'is_dynamic', 'is_run', 'is_virtual_machine', 'memory', 'operating_system', 'os_version', 'physical_server',  'processor', 'roles', 'salt_id', 'status', 'system_name', 'update_time', 'uuid']

class IdcIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Idc
        fields = ['comment', 'company', 'create_time',  'idc_address', 'idc_name',  'is_deleted', 'is_dynamic', 'status', 'update_time']

class IpRecordIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = IpRecord
        fields = ['alias', 'comment', 'create_time', 'ip_address', 'ip_resource',  'is_deleted', 'is_dynamic', 'mask', 'status', 'update_time']

class IpResourceIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = IpResource
        fields = ['alias', 'begin_ip', 'comment', 'create_time', 'dns', 'end_ip', 'gateway', u'id', 'idc_contract', u'idc_contract_id', u'ip_resource_record', 'is_deleted', 'is_dynamic', 'mask', 'operator', 'status', 'update_time']

class NetworkEquipmentIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = NetworkEquipment
        fields = ['asset_num', 'brand', 'comment', 'create_time', 'equipment_type', 'is_deleted', 'is_dynamic', 'is_remote_control', 'is_run', 'manufacturer',  'model_num', 'serial', 'idc_device_num', 'volume', 'order_date', 'order_num', 'price', 'status', 'total_ports', 'update_time', 'uuid', 'warranty_period']

class PhysicalServerIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = PhysicalServer
        fields = ['asset_num', 'brand',  'comment',  'create_time', 'harddisk', u'host_physical_server', u'id',  'is_control_card', 'is_deleted', 'is_dynamic', 'is_run', 'is_virtualization', 'manufacturer',  'memory', 'model_num', 'network_card', 'operating_system', 'order_date', 'order_num', 'price', 'processor', 'serial', 'idc_device_num', 'volume', 'status', 'update_time', 'uuid', 'warranty_period']

