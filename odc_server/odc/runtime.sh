#!/bin/sh

if [ $4 -eq 1 ];then
	docker container run --name $1 -d -p :22 $2
fi
docker cp $3 $1:/home/user/.ssh/authorized_keys
if [ $5 -eq 1 ];then
	docker exec run $1 useradd -m $6