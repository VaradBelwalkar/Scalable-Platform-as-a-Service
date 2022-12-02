#!/bin/sh
scp -r -i $1/bin/keyForRemoteServer -P $3 $2/* root@$4:/var/www/html/
