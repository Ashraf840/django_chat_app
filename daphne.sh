#!/bin/bash

echo "running daphne.sh file!"
echo "User: $USER"
echo "Present Dir: $PWD"

# Install daphne in host machine
sudo apt install daphne -y

# Activate python env
source env/bin/activate

# Check if daphne_access.log & daphne_error.log exist, otherwise create the files.
if [ -e logs/daphne_access.log ] && [ -e logs/daphne_error.log ]
then
    echo "'daphne_access.log' & 'daphne_error.log' files exist!"
else
    touch logs/daphne_access.log logs/daphne_error.log
    sudo chmod u+x logs/daphne_access.log logs/daphne_error.log
    echo "Created the 'daphne_access.log' & 'daphne_error.log' file!"
fi

# Check if the '/etc/systemd/system/teachatty_chat_app_daphne.socket' file exists, otherwise create the file
if [ -e /etc/systemd/system/teachatty_chat_app_daphne.socket ]
then
    echo "teachatty_chat_app_daphne.socket file exists"
else
    echo "teachatty_chat_app_daphne.socket file doesn't exists"
    sudo cp -rf teachatty_chat_app_daphne.socket /etc/systemd/system/teachatty_chat_app_daphne.socket
    echo "Copied teachatty_chat_app_daphne.socket file into path: /etc/systemd/system/teachatty_chat_app_daphne.socket"
fi
sudo chown -R jenkins /etc/systemd/system/teachatty_chat_app_daphne.socket

# Check if the '/etc/systemd/system/teachatty_chat_app_daphne.service' file exists, otherwise create the file
if [ -e /etc/systemd/system/teachatty_chat_app_daphne.service ]
then
    echo "teachatty_chat_app_daphne.service file exists"
else
    echo "teachatty_chat_app_daphne.service file doesn't exists"
    sudo cp -rf teachatty_chat_app_daphne.service /etc/systemd/system/teachatty_chat_app_daphne.service
    echo "Copied teachatty_chat_app_daphne.service file into path: /etc/systemd/system/teachatty_chat_app_daphne.service"
fi
sudo cp -rf teachatty_chat_app_daphne.service /etc/systemd/system/teachatty_chat_app_daphne.service
sudo chown -R jenkins /etc/systemd/system/teachatty_chat_app_daphne.service

sudo systemctl daemon-reload
sudo systemctl start teachatty_chat_app_daphne.socket
sudo systemctl enable teachatty_chat_app_daphne.socket

echo "teachatty_chat_app_daphne is about to be started!"

sudo systemctl restart teachatty_chat_app_daphne.socket
sudo systemctl restart teachatty_chat_app_daphne.service
sudo systemctl enable teachatty_chat_app_daphne.service
sudo systemctl status teachatty_chat_app_daphne.socket
sudo systemctl status teachatty_chat_app_daphne.service

echo "Daphne setup finished!"