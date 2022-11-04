#!/bin/bash

echo "running uwsgi.sh file!"
echo "User: $USER"
echo "Present Dir: $PWD"

# Install uwsgi in the python env
source env/bin/activate
pip3 install uwsgi

# Check if '/var/lib/jenkins/workspace/teachatty_chat_app/logs/teachatty_uwsgi.log' file exist, otherwise create the file
if [ -e /var/lib/jenkins/workspace/teachatty_chat_app/logs/teachatty_uwsgi.log ]
then
    echo "teachatty_uwsgi.log file exists"
else
    echo "teachatty_uwsgi.log file doesn't exists"
    touch logs/teachatty_uwsgi.log
    echo "Created the teachatty_uwsgi.log file into path: $PWD/logs/teachatty_uwsgi.log"
fi

# Check if the 'vassals' dir exists, otherwise create the dir
if [ -d /etc/uwsgi/vassals ]
then
    echo "vassals dir exists"
else
    echo "vassals dir doesn't exists"
    sudo mkdir /etc/uwsgi/vassals
    echo "Created '/etc/uwsgi/vassals' dir!"
fi
sudo chown -R jenkins /etc/uwsgi/vassals

sudo systemctl daemon-reload
sudo systemctl restart uwsgi.service
sudo systemctl status uwsgi.service
sudo systemctl restart emperor.uwsgi.service
sudo systemctl status emperor.uwsgi.service

echo "Uwsgi setup finished!"

