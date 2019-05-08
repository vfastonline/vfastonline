#!/usr/bin/env bash

basepath=$(cd `dirname $0`; pwd)

# 多服务器用空格分隔
SERVERS="172.16.155.128"
PASSWORD=123456

auto_ssh_copy_id() {
    expect -c "set timeout -1;
        spawn ssh-copy-id root@$1; 
        expect {
            *(yes/no)* {send -- yes\r;exp_continue;}
            *assword:* {send -- $2\r;exp_continue;}
            eof        {exit 0;}
        }";
}

ssh_copy_id_to_all() {
    for SERVER in $SERVERS
    do
        auto_ssh_copy_id $SERVER $PASSWORD
    done
}

ssh_copy_id_to_all


for SERVER in $SERVERS
do
    scp -r deploy.sh root@$SERVER:/root/
    scp -r m.conf root@$SERVER:/root/
    scp -r openresty_repo root@$SERVER:/root/
    scp -r uwsgi root@$SERVER:/root/
    scp -r vfast-1.0.tar.gz root@$SERVER:/root/
    scp -r media root@$SERVER:/root/
    scp -r vfast.sql root@$SERVER:/root/
    scp -r Python-2.7.2.tar.bz2 root@$SERVER:/root/
    ssh root@$SERVER /root/deploy.sh $SERVER
done