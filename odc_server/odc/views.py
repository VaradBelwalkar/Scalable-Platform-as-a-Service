# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from .forms import DocumentForm
from .forms import DocumentfolderForm
from .models import Document
from .models import Details
from .models import runtimeDetails
import hashlib
import subprocess
import shlex
import sys
import docker
import os
import pathlib
import json
import time
import socket

def home(request):
    user = request.user
    if user.is_authenticated:
        documents = Document.objects.filter(username=request.user.username)
        check = Details.objects.filter(username=request.user.username).exists()
        if not check:
            p = Details(username=user)
            p.save()
        details = Details.objects.get(username=request.user.username)
        return render(request, 'home.html', {'documents': documents, 'details': details})
    else:
        return redirect('login')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy(viewname='login')
    template_name = 'signup.html'


def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        filepath = form.data['filepath']
        files = request.FILES.getlist('document')
        username = request.user.username
        for doc in files:
            na = doc.name
            hashf = hashlib.md5()
            blocksize = 65536
            for block in iter(lambda: doc.read(blocksize), b""):
                hashf.update(block)
            md5sum = str(hashf.hexdigest())
            check = Document.objects.filter(username=request.user.username, name=na, filepath=filepath).exists()
            if check:
                Document.objects.filter(username=request.user.username, name=na, filepath=filepath).delete()
            p = Document(name=na, filepath=filepath, document=doc, username=username, md5sum=md5sum)
            p.save()
        return redirect('home')
    else:
        user = request.user
        if user.is_authenticated:
            form = DocumentForm()
            return render(request, 'upload.html', {
            'form': form
            })
        else:
            return redirect('login')


def delete(request, id):
    user = request.user
    if user.is_authenticated:
        Document.objects.filter(username=request.user.username, id=id).delete()
        return redirect('home')
    else:
        return redirect('login')

def deadlocksetfalse(request):
    user = request.user
    if user.is_authenticated :
        Details.objects.filter(username=request.user.username).update(in_sync=False)
        return redirect('home')
    else:
        return redirect('login')


def deadlocksettrue(request):
    user = request.user
    if user.is_authenticated :
        Details.objects.filter(username=request.user.username).update(in_sync=True)
        return redirect('home')
    else:
        return redirect('login')


def upload_folder(request):
    if request.method == 'POST':
        form = DocumentfolderForm(request.POST, request.FILES)
        filepath = form.data['filepath']
        files = request.FILES.getlist('document')
        username = request.user
        for doc in files:
            na=doc.name
            p = Document(name=na, filepath=filepath, document=doc, username=username)
            p.save()
        return redirect('home')
    else:
        user = request.user
        if user.is_authenticated:
            form = DocumentfolderForm()
            return render(request, 'upload.html', {
            'form': form
            })
        else:
            return redirect('login')


#view to get a new container access for a specific image
def run_containers(request,requestedImage):
    htmlInfo = """<html><head></head><body><div><a href="info">{}</a></div></body></html>"""
    htmlResponse =  """<html><head></head><body><div><a href="port">{}</a><a href="privatekey">{}</a></div></body></html>"""
    projectPath = pathlib.Path(__file__).parent.parent.resolve()
    try:
       os.remove('{}/id_rsa'.format(projectPath)) 
       os.remove('{}/id_rsa.pub'.format(projectPath))
    except IOError:
        pass
    containerUser={}
    if not request.user.is_authenticated:        
         return HttpResponse(htmlInfo.format("Authentication failed !"))            

    user = request.user.username
    check = runtimeDetails.objects.filter(username=user).exists()
    if not check:
        containerUser = runtimeDetails(username = user ,ownedContainers = "{}",totalOwnedContainers = 0)
        containerUser.save()
    else:
        containerUser = runtimeDetails.objects.get(username = user)
 
    if(containerUser.totalOwnedContainers >= 5):
        return HttpResponse(htmlInfo.format("Sorry! Currently we cannot allocate more than 5 container runtimes to single user ! Try removing the unnecessary container to start a new one"))
    else:
        client = docker.from_env()
        subprocess.run(["{}/odc/runtime.sh".format(projectPath),"{}".format(user),"{}".format(requestedImage),"1","0"])
        containerObj = client.containers.get(user)
        portChoice = containerObj.attrs['NetworkSettings']['Ports']['22/tcp'][0]['HostPort']
        subprocess.run(["{}/odc/updateName.sh".format(projectPath),"{}".format(user),"{}_{}".format(user,portChoice)])
        containerListInDict = json.loads(containerUser.ownedContainers)
        containerListInDict["{}_{}".format(user,portChoice)] = "running"
        containerUser.ownedContainers = json.dumps(containerListInDict)
        containerUser.totalOwnedContainers += 1
        containerUser.save()

        fp=open("{}/id_rsa".format(projectPath),'r')
        privateKey=fp.read()
        fp.close()
        os.remove('{}/id_rsa'.format(projectPath))
        os.remove('{}/id_rsa.pub'.format(projectPath))

        return HttpResponse(htmlResponse.format(portChoice,privateKey))



def start_containers(request,containerName):
        htmlInfo = """<html><head></head><body><div><a href="info">{}</a></div></body></html>"""
        htmlResponse =  """<html><head></head><body><div><a href="port">{}</a><a href="privatekey">{}</a></div></body></html>"""
        projectPath = pathlib.Path(__file__).parent.parent.resolve()
        try:
           os.remove('{}/id_rsa'.format(projectPath)) 
           os.remove('{}/id_rsa.pub'.format(projectPath))
        except IOError:
           pass
        containerUser={}
        client = docker.from_env()
        if not request.user.is_authenticated:        
             return HttpResponse(htmlInfo.format("Authentication failed !"))            
    
        user = request.user.username
        check = runtimeDetails.objects.filter(username=user).exists()
        if not check:
            return HttpResponse(htmlInfo.format("You haven't run any containers yet. Try one by using \"run <runtime_name>\" command"))    
        containerUser = runtimeDetails.objects.get(username = user)
        if (containerUser.totalOwnedContainers >0):
            containerObj = client.containers.get(containerName)
            containerListInDict = json.loads(containerUser.ownedContainers)
            if(containerListInDict[containerName] == "stopped"):                
                containerObj.start()
                del containerListInDict[containerName]
            containerObj.exec_run(cmd="rm /home/user/.ssh/authorized_keys")
            subprocess.run(["{}/odc/runtime.sh".format(projectPath),"{}".format(containerName),"{}".format("dummy_value"),"0","0"])
            fp=open("{}/id_rsa".format(projectPath),'r')
            privateKey=fp.read()
            fp.close()
            containerObj = client.containers.get(containerName)
            portChoice = containerObj.attrs['NetworkSettings']['Ports']['22/tcp'][0]['HostPort']
            subprocess.run(["{}/odc/updateName.sh".format(projectPath),"{}".format(containerName),"{}_{}".format(user,portChoice),"0"])
            
            containerListInDict["{}_{}".format(user,portChoice)] = "running"
            containerUser.ownedContainers =json.dumps(containerListInDict)
            containerUser.save()
            os.remove("{}/id_rsa".format(projectPath))
            os.remove("{}/id_rsa.pub".format(projectPath))

            return HttpResponse(htmlResponse.format(portChoice,privateKey))
        else:
            return HttpResponse(htmlInfo.format("You don't have any running containers currently !"))

def docker_list(request,list_what):
        htmlInfo = """<html><head></head><body><div><a href="info">{}</a></div></body></html>"""
        htmlResponse =  """<html><head></head><body><div><a href="port">{}</a><a href="privatekey">{}</a></div></body></html>"""
        projectPath = pathlib.Path(__file__).parent.parent.resolve()
        containerUser={}
        client = docker.from_env()
        if not request.user.is_authenticated:        
             return HttpResponse(htmlInfo.format("Authentication failed !")) 
        if(list_what == "images"):
            
            return HttpResponse(htmlInfo.format("ubuntu\nbase_ubuntu\ndevelopment_server\nnginx\nalpine"))
        user = request.user.username
        check = runtimeDetails.objects.filter(username=user).exists()
        if not check:
            return HttpResponse(htmlInfo.format("You haven't run any containers yet. Try one by using \"run <runtime_name>\" command"))    
        containerUser = runtimeDetails.objects.get(username = user)
        containerListInDict = json.loads(containerUser.ownedContainers)
        return HttpResponse(htmlInfo.format(containerListInDict))




#Stop or remove the containers
def stop_or_remove_containers(request,stop_or_remove,containerName):
        htmlInfo = """<html><head></head><body><div><a href="info">{}</a></div></body></html>""" 
        projectPath = pathlib.Path(__file__).parent.parent.resolve()
        client = docker.from_env()
        if not request.user.is_authenticated:        
             return HttpResponse(htmlInfo.format("Authentication failed !")) 
        user = request.user.username
        check = runtimeDetails.objects.filter(username=user).exists()
        if (check):
            containerUser = runtimeDetails.objects.get(username = user)
            if (containerUser.totalOwnedContainers > 0):
                containerObj = client.containers.get(containerName)
                containerListInDict = json.loads(containerUser.ownedContainers)
                if (stop_or_remove == "stop"):
                    if(containerListInDict[containerName] == "stopped"):
                        return HttpResponse(htmlInfo.format("Container already stopped !"))
                    containerObj.stop()
                    containerListInDict[containerName] = "stopped"
                    containerUser.ownedContainers = json.dumps(containerListInDict)
                    containerUser.save()
                    return HttpResponse(htmlInfo.format("Container successfully stopped !"))
                containerObj.stop()
                containerObj.remove()
                containerUser.totalOwnedContainers -=1
                del containerListInDict[containerName]
                containerUser.ownedContainers = json.dumps(containerListInDict)
                containerUser.save()              
                return HttpResponse(htmlInfo.format("Container successfully deleted !"))
            else: 
                return HttpResponse(htmlInfo.format("You don't have any running containers currently !"))
        else:
            return HttpResponse(htmlInfo.format("You haven't run any containers yet. Try one by using \"run <runtime_name>\" command"))
     
  
  

def deploy_app_or_website(request,app_or_website,clientusername):
    htmlInfo = """<html><head></head><body><div><a href="info">{}</a></div></body></html>"""
    htmlResponse =  """<html><head></head><body><div><a href="port">{}</a><a href="privatekey">{}</a><a href="websiteinfo">{}</a></div></body></html>"""
    projectPath = pathlib.Path(__file__).parent.parent.resolve()
    try:
       os.remove('{}/id_rsa'.format(projectPath)) 
       os.remove('{}/id_rsa.pub'.format(projectPath))
    except IOError:
        pass
    containerUser={}
    if not request.user.is_authenticated:        
         return HttpResponse(htmlInfo.format("Authentication failed !"))            

    user = request.user.username
    check = runtimeDetails.objects.filter(username=user).exists()
    if not check:
        containerUser = runtimeDetails(username = user ,ownedContainers = "{}",totalOwnedContainers = 0)
        containerUser.save()
    else:
        containerUser = runtimeDetails.objects.get(username = user)
 
    if(containerUser.totalOwnedContainers >= 5):
        return HttpResponse(htmlInfo.format("Sorry! Currently we cannot allocate more than 5 container runtimes to single user ! Try removing the unnecessary container to start a new one"))
    else:
        client = docker.from_env()
        subprocess.run(["{}/odc/runtime.sh".format(projectPath),"{}".format(user),"{}".format(app_or_website),"1","1",clientusername])
        containerObj = client.containers.get(user)
        portChoice = containerObj.attrs['NetworkSettings']['Ports']['22/tcp'][0]['HostPort']
        subprocess.run(["{}/odc/updateName.sh".format(projectPath),"{}".format(user),"{}_{}".format(user,app_or_website)])
        containerListInDict = json.loads(containerUser.ownedContainers)
        containerListInDict["{}_{}".format(user,portChoice)] = "running"
        containerUser.ownedContainers = json.dumps(containerListInDict)
        containerUser.totalOwnedContainers += 1
        containerUser.save()

        fp=open("{}/id_rsa".format(projectPath),'r')
        privateKey=fp.read()
        fp.close()
        os.remove('{}/id_rsa'.format(projectPath))
        os.remove('{}/id_rsa.pub'.format(projectPath))
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        msg = "\t\t\t\tCongratulations!\nYou have deployed your website\nYou can access it by typing following in browser:\n\t\t\t\t{}:{}\n\nIf you want to name the website, run following command :\n\t\twebsite <website-name> <new-name>\n Then you can access the website using http://<new-name>\n\n".format(IPAddr,portChoice)
        return HttpResponse(htmlResponse.format(portChoice,privateKey,msg))


def rename_website(request,oldwebsitename,newwebsitename):
    htmlInfo = """<html><head></head><body><div><a href="info">{}</a></div></body></html>"""
    subprocess.run(["{}/odc/updateName.sh".format(projectPath),"{}".format(oldwebsitename),"{}_{}".format(user,newwebsitename)])
    return HttpResponse(htmlInfo.format("website renamed successfully!\nNow you can access the website by typing:\n\t\t{}\tin browser\n".format(newwebsitename)))