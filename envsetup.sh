#!/bin/bash

echo "running envsetup.sh file!"
echo "User: $USER"
echo "Present Dir: $PWD"

if [ -d "env" ]
then
  echo "Python virtual env exists"
else
  python3 -m venv env
fi

echo "Present Directory: $PWD"
source env/bin/activate

pip3 install -r requirements_linux.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "Django migrations have been done while executing envsetup.sh!"

if [ -d "logs" ]
then
  echo "Log folder exists"
else
  mkdir logs
  touch logs/error.log logs/access.log
fi


sudo chmod -R 777 logs
echo "Env setup finished!"