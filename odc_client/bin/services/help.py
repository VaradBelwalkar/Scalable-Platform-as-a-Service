help = '''
NAME
       ODC : Client to access microservices

DESCRIPTION
ODC :
         odc is a way to access secure personal storage at the server with ability to access various runtimes 
         the server provides with access to some services

ODC STARTUP 
       To get into odc environment, just type,

       $odc start

ODC COMMANDS

       odc $ config

               Displays the configured URL, username, and password of the client

       odc $ config edit

              Edits configuration and saves the changes
	   
	odc $ version

               Shows the version number of the project

       odc $ server

               Shows information about the server

       odc $ signup

              Creates an account with given username and password

       odc $ view
      
              lists all the files in the cloud

       odc $ uploadfile <file-path>

              uploads the specified file into the cloud

       odc $ uploaddir <dir-path>

              uploads the specified directory to the cloud

       odc $ download <filename> <filepath>

              downloads the specified file from the cloud

       odc $ delete <filepath>+'/'+<filename>

              deletes the specified file in the cloud

       odc $ sync <dirpath>

              sync the specified directory with the cloud



ODC COMMANDS TO ACCESS RUNTIMES

  (CURRENTLY AVAILABLE RUNTIMES : "ubuntu" , "development_server")

  (You can own maximum of 5 containers at a time)


       odc $ container  run <runtime_name> 
             
              get a new specifed container

       odc $ container list images

              get available os images

       odc $ container list containers

              get the list of containers that you own (useful for which container to resume)

       odc $ container resume <container_name>

              get the specified container that you own from your owned_containers list

       odc $ container stop <container_name>/all

              stop the specified container or all  on server side

       odc $ container remove <container_name>/all

              remove the specified container or all from the server

'''       
print(help)