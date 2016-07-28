#!/bin/bash

python_path=/usr/local/python27
python_bin=${python_path}/bin
python_prog=${python_bin}/python
django_admin_prog=${python_bin}/django-admin.py 

vi_prog='/bin/vi'

if [[ -f '/usr/bin/vim' ]];then
    vi_prog=/usr/bin/vim
fi


function get_curr_real_path(){
    local c_p=$(pwd)
    cd $(dirname ${BASH_SOURCE:-$0})
    local d_p=$(pwd)
    cd ${c_p}
    echo ${d_p}
}

proj_path=$(get_curr_real_path)

proj_path=${proj_path}/../

app_path=${proj_path}/cmdb

app_trans_file=${app_path}/locale/zh_CN/LC_MESSAGES/django.po

curr_path=$(/bin/pwd)

function compilemessages() {
    cd ${app_path}
    ${django_admin_prog} compilemessages
}

if [[ $1 == 'edit' ]];then
    ${vi_prog}  ${app_trans_file}
    compilemessages
else
    compilemessages
fi

cd ${curr_path}
