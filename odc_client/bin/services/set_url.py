import pickle
import sys
import pathlib
projectPath = pathlib.Path(__file__).parent.parent.parent.resolve()
data = dict()
ipAddr = input("Enter server IP :")
portno = input("Enter server port to access :")\

try:
    f = open('{}/bin/odc_user_data'.format(projectPath), 'rb')
    data = pickle.load(f)
    f.close()
except IOError:
    print("You are setting up URL. RUN '$config edit' to set up username and password ")

data['portno'] = portno
data['ipAddr'] = ipAddr
data['url'] = "http://{}:{}/".format(ipAddr,portno)
f = open('{}/bin/odc_user_data'.format(projectPath), 'wb')
pickle.dump(data,f)
f.close()
print("URL saved")
