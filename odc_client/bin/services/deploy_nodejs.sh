#!/bin/sh
scp -r -i $1/bin/keyForRemoteServer -P $3 $2/* user@$4:~/nodejsapp/
