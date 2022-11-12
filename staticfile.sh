#!/bin/bash

echo "running nginx.sh file"
echo "User: $USER"
echo "Present Directory: $PWD"


# Check for the folder directory & copy the staticfiles to /var/www/projects_static
if [ -d /var/www/projects_static ]
then
    echo "/var/www/projects_static dir exist!"
else
    echo "projects_static dir doesn't exist! Created the dir!"
    mkdir /var/www/projects_static
    # Check the teachatty_chat_app dir inside /var/www/projects_static, otherwise create
    if [ -d /var/www/projects_static/teachatty_chat_app ]
    then
      echo "teachatty_chat_app dir exist!"
    else
      echo "teachatty_chat_app dir doesn't exist! Created the dir!"
      mkdir /var/www/projects_static/teachatty_chat_app
    fi
fi
