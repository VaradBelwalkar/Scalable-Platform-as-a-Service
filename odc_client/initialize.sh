SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
cd "$SCRIPTPATH"
echo $SCRIPTPATH
sudo cp -s $SCRIPTPATH/bin/odc1-client /usr/bin/odc-client && chmod 755 /usr/bin/odc-client
