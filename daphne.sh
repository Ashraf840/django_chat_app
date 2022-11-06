#!/bin/bash

echo "running daphne.sh file!"
echo "User: $USER"
echo "Present Dir: $PWD"

# Install daphne in host machine
sudo apt install daphne -y

# Activate python env
source env/bin/activate

# Check if the '/etc/systemd/system/teachatty_chat_app_daphne.service' file exists, otherwise create the file
if [ -e /etc/systemd/system/teachatty_chat_app_daphne.service ]
then
    echo "teachatty_chat_app_daphne.service file exists"
else
    echo "emperor.uwsgi.service file doesn't exists"
    sudo cp -rf teachatty_chat_app_daphne.service /etc/systemd/system/teachatty_chat_app_daphne.service
    echo "Copied teachatty_chat_app_daphne.service file into path: /etc/systemd/system/teachatty_chat_app_daphne.service"
fi
sudo chown -R jenkins /etc/systemd/system/teachatty_chat_app_daphne.service

sudo systemctl daemon-reload
sudo systemctl start teachatty_chat_app_daphne.service
sudo systemctl status teachatty_chat_app_daphne.service

echo "Daphne setup finished!"