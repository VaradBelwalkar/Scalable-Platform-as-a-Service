import pickle
from getpass import getpass
import pathlib
import sys
projectPath = pathlib.Path(__file__).parent.parent.parent.resolve() 
set_url='http://127.0.0.1:8000/'
try:
    f = open('{}/bin/odc_user_data'.format(projectPath),'rb')
    data = pickle.load(f)
    set_url = data['url']
    print("using existing server URL...\n")
except IOError:
    print("You haven't configured anything yet,wil be using localhost server URL...\n\n")

Username = input("Enter Username:")
Password = getpass("Enter Password:")
Password2 = getpass("Confirm Password:")
if Password != Password2:
    while Password != Password2:
        print("Your Password does not match. Please try again")
        Password = getpass("Enter Password:")
        Password2 = getpass("Confirm Password:")
        print("Configure server URL using the command $ set url")
data = dict(username=Username, password=Password, url=set_url)
f = open('{}/bin/odc_user_data'.format(projectPath), 'wb')
pickle.dump(data, f)
print("User credentials updated")
f.close()
