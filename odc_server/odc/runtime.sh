#!/bin/sh

if [ $3 -eq 1 ];then
	docker container run --name $1 -d -p :22 $2
fi
ssh-keygen -f "./id_rsa" -t rsa -q -N ""
docker cp ./id_rsa.pub $1:/home/user/.ssh/authorized_keys
if [ $4 -eq 1 ];then
	docker exec run $1 useradd -m $5