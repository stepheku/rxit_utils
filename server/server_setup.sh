#!/usr/bin/env bash

# Consider running these two commands separately
# Do a reboot before continuing.
sudo apt update
sudo apt upgrade -y

# Install some OS dependencies:
sudo apt install -y -q build-essential git 
sudo apt install -y -q python3-pip python3-dev python3-venv
sudo apt install -y -q unzip wget git
sudo apt install -y -q nginx
# for gzip support in uwsgi
sudo apt install --no-install-recommends -y -q libpcre3-dev libz-dev nload

# Stop the hackers
sudo apt install fail2ban -y

sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Create separate app credentials
sudo adduser app
sudo usermod -aG sudo app

su app

# Basic git setup
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=720000'

# Be sure to put your info here:
git config --global user.email "stepheku@users.noreply.github.com"
git config --global user.name "stepheku"

# Web app file structure
mkdir /home/app/apps
# chmod 777 /home/app/apps
mkdir /home/app/apps/logs
mkdir /home/app/apps/logs/rxit_utils
mkdir /home/app/apps/logs/rxit_utils/app_log
cd /home/app/apps

# Create a virtual env for the app.
cd /home/app/apps
python3 -m venv venv
source /home/app/apps/venv/bin/activate
pip install --upgrade pip setuptools
pip install --upgrade httpie glances
pip install --upgrade uwsgi

# clone the repo:
cd /home/app/apps
git clone https://github.com/stepheku/rxit_utils

# Setup the web app:
cd /home/app/apps/rxit_utils
# pip install -r requirements.txt
python setup.py develop

# Copy and enable the daemon
sudo cp /home/app/apps/rxit_utils/server/rxit_utils.service /etc/systemd/system/

sudo systemctl start rxit_utils
sudo systemctl status rxit_utils
sudo systemctl enable rxit_utils

# Setup the public facing server (NGINX)
sudo apt install nginx

# CAREFUL HERE. If you are using default, maybe skip this
sudo rm /etc/nginx/sites-enabled/default

cp /home/app/apps/rxit_utils/server/rxit_utils.nginx /etc/nginx/sites-enabled/rxit_utils.nginx
update-rc.d nginx enable
service nginx restart
