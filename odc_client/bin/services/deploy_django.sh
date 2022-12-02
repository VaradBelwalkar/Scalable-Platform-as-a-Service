#!/bin/sh
scp -r -i $1/bin/keyForRemoteServer -P $3 $2/* $(whoami)@$4:$2/
