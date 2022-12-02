import pickle
import sys
import pathlib

projectPath = pathlib.Path(__file__).parent.parent.parent.resolve()

data = dict()
try:
    f = open('{}/bin/odc_user_data'.format(projectPath), 'rb')
    data = pickle.load(f)
except IOError:
    print("The file with user data is either missing or corrupted")
    print("You can use '$ config edit' to reconfigure user data")
    sys.exit()
print("Server URL:" + str(data['url']))
print("Username:" + str(data['username']))
#print("Password:" + str(data['password']))
