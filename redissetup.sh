#!/bin/bash

echo "running envsetup.sh file!"
echo "User: $USER"
echo "Present Dir: $PWD"

# Install & restart redis
sudo apt install redis-server
sudo systemctl restart redis

# View network conn for TCP, routing tables, network interface & network protocol statsistics
sudo apt install net-tools
sudo netstat -lnp | grep redis

# Check redis status
sudo systemctl status redis

echo "Redis setup finished!"


