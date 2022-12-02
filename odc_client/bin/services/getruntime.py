import pickle
import sys
import requests
from getpass import getpass
import subprocess
import os
from bs4 import BeautifulSoup
import pathlib
projectPath = pathlib.Path(__file__).parent.parent.parent.resolve()    
data = dict()

red = '\033[91m'
green = '\033[92m'
end_c = '\033[0m'
base_url = ""
try:
    print("Reading User information ...", end="      ")
    f = open("{}/bin/odc_user_data".format(projectPath), 'rb')
    data = pickle.load(f)
    base_url = data['url']
    print("done")
except IOError:
    print(red+"Authentication credentials not found"+end_c)
    u = input("Enter Username :")
    p = getpass("Enter Password :")
    ipAddr = input("Enter Server IP :")
    portno = intput("Enter server port to access : ")
    data['username'] = u
    data['password'] = p
    data['ipAddr'] = ipAddr
    data['portno'] = portno
    data['url'] = "http://{}:{}/".format(ipAddr,portno)
    base_url = data['url']
    save = input('Would you like to save the configuration? [y/n]:')
    if save == 'y' or save == 'Y':
        f = open("{}/bin/odc_user_data".format(projectPath),'wb')
        pickle.dump(data,f)
        print("User credentials updated")
        f.close()
url = base_url + 'login/'
client = requests.session()
try:
    print("connecting to server ...", end="      ")
    client.get(url)
    print("done")
except requests.ConnectionError as e:
    print(red+"The following error occured connecting to the server: {}\n Please try again".format(e)+end_c)
    client.close()
    sys.exit()

try:
    csrf = client.cookies['csrftoken']
except():
    print(red+"Error obtaining csrf token"+end_c)
    client.close()
    sys.exit()
payload = dict(username=data['username'], password=data['password'], csrfmiddlewaretoken=csrf, next='/')
try:
    sshPortNo=0
    privateKey="not set"
    print("Sending request ...")
    r = client.post(url, data=payload, headers=dict(Referer=url))
    r.raise_for_status()

    if r.status_code == 200:
        print("Request sent ...")
        if r.url == url:
            print(red+"User authentication failed. Please try again"+end_c)
            client.close()
            sys.exit()
        print("Request sent for "+sys.argv[2]+" runtime"+" ...")
    r1 = client.get(base_url + "container/{}/{}/".format(sys.argv[1],sys.argv[2]))
    soup = BeautifulSoup(r1.text, 'html.parser')
    productDivs = soup.findAll('a')
    var = base_url
    for link in productDivs:
        if link['href'] == "port":
            sshPortNo=link.string
        if link['href'] == "privatekey":
            privateKey=link.string
        if link['href'] == "info":
            print(link.string)
            sys.exit()
    fp=open("{}/bin/keyForRemoteServer".format(projectPath),'w')
    fp.write(privateKey)
    fp.close()

    print("\n\nTrying to connect to remote container...\n\n")
    try:
        subprocess.run(["{}/bin/services/connectToRemoteContainer.sh".format(projectPath),"{}".format(projectPath),"{}".format(sshPortNo),"{}".format(data['ipAddr']),"1","{}".format(sys.argv[3])])
    except IndexError:
        print("PYTHON DIDN'T TOOK ARG 4!!!!!!!!")
        subprocess.run(["{}/bin/services/connectToRemoteContainer.sh".format(projectPath),"{}".format(projectPath),"{}".format(sshPortNo),"{}".format(data['ipAddr']),"0"])

except requests.exceptions.HTTPError as e:
    print(red+'HTTP error: {}'.format(e)+end_c)
except requests.exceptions.RequestException as e:
    print(red+'Connection Error: {}'.format(e)+end_c)
    client.close()
    sys.exit()

client.close()
