#!/bin/bash

if [ -z $(shell which pip) ]; then
    sudo apt-get install python-pip
    sudo pip install flake8
fi

if [ -z $(shell which virtualenv) ]; then
    sudo apt-get install python-virtualenv
fi

if [ -z $(shell which nodejs) ]; then
    curl -sL https://deb.nodesource.com/setup | sudo bash -
    sudo apt-get install -y nodejs
fi

if [ -z $(shell which bower) ]; then
    npm install -g bower
fi

if [ -z $(shell which lessc) ]; then
    npm install -g less
fi


if [ ! -d "temp" ]; then
    virtualenv temp
fi

. temp/bin/activate
pip install -r requirements

