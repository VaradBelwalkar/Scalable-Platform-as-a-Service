#!/bin/sh
if [ $4 -eq "1" ];then
sshfs -p $2 -o IdentityFile=$1/bin/keyForRemoteServer,dir_cache=no user@$3:/home/user/ $5
fi
ssh -i $1/bin/keyForRemoteServer -p "$2" user@$3
umount -f $5