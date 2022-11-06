#!/bin/bash

echo "running uwsgi.sh file!"
echo "User: $USER"
echo "Present Dir: $PWD"

# Activate & install uwsgi in the python env
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

# Check if the '/etc/uwsgi/emperor.ini' file exists, otherwise create the file
if [ -e /etc/uwsgi/emperor.ini ]
then
    echo "emperor.ini file exists"
else
    echo "emperor.ini file doesn't exists"
    sudo cp -rf emperor.ini /etc/uwsgi/emperor.ini
    echo "Copied the emperor.ini file into path: /etc/uwsgi/emperor.ini"
fi
sudo chown -R jenkins /etc/uwsgi/emperor.ini

# Check if the '/etc/systemd/system/emperor.uwsgi.service' file exists, otherwise create the file
if [ -e /etc/systemd/system/emperor.uwsgi.service ]
then
    echo "emperor.uwsgi.service file exists"
else
    echo "emperor.uwsgi.service file doesn't exists"
    sudo cp -rf emperor.uwsgi.service /etc/systemd/system/emperor.uwsgi.service
    echo "Copied emperor.uwsgi.service file into path: /etc/systemd/system/emperor.uwsgi.service"
fi
sudo chown -R jenkins /etc/systemd/system/emperor.uwsgi.service

# Check if the '/etc/uwsgi/teachatty.ini' file exists, otherwise create the file
if [ -e /etc/uwsgi/vassals/teachatty.ini ]
then
    echo "teachatty.ini file exists"
else
    echo "teachatty.ini file doesn't exists"
    sudo cp -rf teachatty.ini /etc/uwsgi/vassals/teachatty.ini
fi
sudo cp -rf teachatty.ini /etc/uwsgi/vassals/teachatty.ini
echo "Copied teachatty.ini file to path: /etc/uwsgi/vassals/teachatty.ini"
sudo chown -R jenkins /etc/uwsgi/vassals/teachatty.ini

sudo systemctl daemon-reload
sudo systemctl restart uwsgi.service
sudo systemctl status uwsgi.service
sudo systemctl restart emperor.uwsgi.service
sudo systemctl status emperor.uwsgi.service

echo "Uwsgi setup finished!"

