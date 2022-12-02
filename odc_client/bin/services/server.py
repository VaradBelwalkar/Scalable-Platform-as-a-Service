import requests
import pickle
import pathlib
import sys
projectPath = pathlib.Path(__file__).parent.parent.parent.resolve()
data = dict()
try:
    print("Reading Server information ...")
    f = open('{}/bin/odc_user_data'.format(projectPath), 'rb')
    data = pickle.load(f)
except IOError:
    print("Server details not found. Use the command $ set url to configure server details")
    
url = data['url']
r = requests.get(url)
print(r.headers['Server'])
