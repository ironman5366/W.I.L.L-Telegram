#!/usr/bin/env bash
#Standalone setup script for W.I.L.L
if ! dpkg -s python-pip; then
    echo "pip not installed, installing"
    sudo apt-get install pip
fi

if ! dpkg -s git; then
    echo "git not installed, installing"
    sudo apt-get install git
fi

cd /usr/local

echo "Downloading latest version of W.I.L.L"

git clone "https://github.com/ironman5366/W.I.L.L-Telegram"

cd W.I.L.L-Telegram

echo "Installing required python modules"

sudo pip install -r requirements.txt

python dbsetup.py

echo "Setting up W.I.L.L as service"

cp will.conf /etc/init/will.conf

echo "Reloading services"

sudo initctl reload-configuration

echo "Finished installation. To start W.I.L.L, run sudo start will"
