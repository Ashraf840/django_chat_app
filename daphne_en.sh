#!/bin/bash

echo "running daphne_en.sh file!"
echo "This shell-script is run by 'teachatty_chat_app_daphne.service' file"
echo "User: $USER"
echo "Present Dir: $PWD"

source env/bin/activate
daphne -b 0.0.0.0 -p 8001 chatSystem.asgi:application