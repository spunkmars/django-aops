model_list='
        device:Device
        idc_contract:IdcContract
        cdn:Cdn
        brand:Brand
        cabinet:Cabinet
        cabinet_seat:CabinetSeat
        cdn_domain_record:CdnDomainRecord
        company:Company
        contacts:Contacts
        contract:Contract
        domain_name:DomainName
        domain_record:DomainRecord
        host:Host
        idc:Idc
        ip_record:IpRecord
        ip_resource:IpResource
        network_equipment:NetworkEquipment
        physical_server:PhysicalServer
'

for i in `echo ${model_list}`
do
    a=`echo $i|awk -F ":" '{print $1}'`
    b=`echo $i|awk -F ":" '{print $2}'`


   echo "from cmdb.models.${a} import $b"
done

for i in `echo ${model_list}`
do
    a=`echo $i|awk -F ":" '{print $1}'`
    b=`echo $i|awk -F ":" '{print $2}'`

    c=`cat ./fields.list|awk -F ":" -v b=$b 'b == $1{print $2}'`

   echo "class ${b}Index(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = ${b}
        fields = ${c}
"
done
