#!/usr/bin/env bash

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
    scp -r /Users/xuhuiliang/Downloads/vfast_install root@$SERVER:/root/
    echo "/root/vfast_install/deploy.sh $SERVER"
    ssh root@$SERVER /root/vfast_install/deploy.sh $SERVER
done