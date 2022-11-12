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
    sudo mkdir /var/www/projects_static
fi

# Check the teachatty_chat_app dir inside /var/www/projects_static, otherwise create
if [ -d /var/www/projects_static/teachatty_chat_app ]
then
    echo "teachatty_chat_app dir exist!"
else
    echo "teachatty_chat_app dir doesn't exist! Created the dir!"
    sudo mkdir /var/www/projects_static/teachatty_chat_app
fi

# Copy the staticfiles dir to /var/www/projects_static/teachatty_chat_app
sudo cp -R /var/lib/jenkins/workspace/teachatty_chat_app/staticfiles /var/www/projects_static/teachatty_chat_app
sudo chown -R root staticfiles

# Remove staticfiles from /var/lib/jenkins/workspace/teachatty_chat_app
sudo rm -rf /var/lib/jenkins/workspace/teachatty_chat_app/staticfiles
