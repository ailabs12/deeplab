#!/bin/bash

#RUN THE SCRIPT IN THE PROJECT FOLDER: deeplab

chmod +x install.sh

a=`sudo docker-compose --version`
echo $a
 
if [[ "$a" != *1.22.0-rc2* ]]
then
	echo "Installation docker-compose"
	#delete docker-compose
	sudo rm /usr/local/bin/docker-compose
	sudo pip uninstall docker-compose
	#install version 1.22.0-rc2
	sudo curl -L https://github.com/docker/compose/releases/download/1.22.0-rc2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
	chmod +x /usr/local/bin/docker-compose
fi

if [[ "$a" == *1.22.0-rc2* ]]
then
	echo "Docker-compose installed"
else
	echo "Error! Docker-compose version 1.22.0-rc2 not installed"
fi 

b=`sudo docker images`

if [[ "$b" != *py2_with_pillow* ]]
then
	echo "Installation image"
	sudo docker build -t py2_with_pillow .
fi

if [[ "$b" == *py2_with_pillow* ]]
then
	echo "Image installed"
else
	echo "Error! Image py2_with_pillow is not installed"
fi

#---- Change docker-compose.yml parameter volumes: ... ----
#Get the path of the directory from which the script is run
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
#Check the presence of the file docker-compose.yml in the current directory
if [ -f $parent_path/docker-compose.yml ];
then
	#Replacement path volumes in docker-compose.yml
	sed -i 's|/home/bka2/models-master/research/deeplab|'$parent_path'|g' docker-compose.yml
else
	echo “File docker-compose.yaml not found”
fi

read -sn1 -p "Press any key to continue..."; echo

