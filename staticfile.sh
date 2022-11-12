#!/bin/bash

echo "running nginx.sh file"
echo "User: $USER"
echo "Present Directory: $PWD"


# Check for the folder directory & copy the staticfiles to /var/www/projects_static
if [ -d /var/www/projects_static ]
then
    echo "/var/www/projects_static dir exist!"
else
    mkdir /var/www/projects_static
fi
