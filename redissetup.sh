#!/bin/bash

echo "running envsetup.sh file!"
echo "User: $USER"
echo "Present Dir: $PWD"



# Check redis-server status
sudo systemctl status redis

echo "Redis setup finished!"


