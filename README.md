# odc
***********Prerequisites***********
 You must have docker-engine installed and the user added to docker group, if not do following
 
    #for ubuntu based distros
      sudo apt-get install openssh-server
      sudo usermod -aG docker <username>
    
    #for arch-based distros
      sudo pacman -S openssh
      sudo usermod -aG docker <username>

HOW TO RUN 

You can run the server and client independently on any systems meeting requirements

TO RUN SERVER DO FOLLOWING :

  1.Download or clone the odc_server into your system\
  2.Just cd into the odc_server and run source bin/activate (Run exactly what specified from the same directory)\
  3.Now run python3 manage.py runserver \
Your server should have now be started

TO RUN CLIENT DO FOLLOWING :

  1.Download or clone the odc_client into your system\
  2.cd into teh odc_client and run source bin/activate (Run exactlt what specified from the same directory)\
  3. cd into bin and run "./odc start"

Now create your credentials by running "config_edit"\
then run "set_url" and set the url for the server\
Now run signup to signup to the service\
Now the client is ready!\
Run "help" to see what you can do

Creadentials in django
by default a user with (for testing),\
username = "odc_user"\
email = "odc_user@example.com"\
password = "odc"

has been created so you can directly login from client without signing in (make sure to update the user credentials in client)
