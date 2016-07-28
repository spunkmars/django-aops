#!/bin/bash

index_dir="templates/search/indexes/cmdb"

suffix="_text.txt"

for file in `ls cmdb/models/*.py|grep -v -P '__init__.py|common.py'`
do

	echo "------${file}------"
        e_file=`echo "${file}"|sed 's/_//g'`
       
	txt_file=`echo ${e_file}|awk -F "/" '{sub(".py","",$NF);sub("_","",$NF);print $NF}'`${suffix}
	
	echo ${txt_file}
	#echo "<h2>{{ object.name }}</h2>" > ${index_dir}/${txt_file}
	for i  in `grep -Po '[^ ]*(?=[ ]*=[ ]*models.)' ${file}`
	do
		echo "<p>{{ object.${i} }}</p>" >> ${index_dir}/${txt_file}
	done
done

