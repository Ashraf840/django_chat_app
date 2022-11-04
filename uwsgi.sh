#!/bin/bash

echo "running uwsgi.sh file!"
echo "User: $USER"
echo "Present Dir: $PWD"

# Install uwsgi in the python env
source env/bin/activate
pip3 install uwsgi




sudo systemctl daemon-reload
sudo systemctl restart uwsgi.service
sudo systemctl status uwsgi.service
sudo systemctl restart emperor.uwsgi.service
sudo systemctl status emperor.uwsgi.service

echo "Uwsgi setup finished!"

