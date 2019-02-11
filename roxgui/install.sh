#!/bin/bash
#
# encoding: utf-8
#
# Install ROXcomposer and its GUI.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

# TODO: Install ROXcomposer-Backend.

# Install Python dependencies.
sudo apt install python3 python3-pip
pip3 install -r requirements.txt

# Go to local project folder.
cd roxgui

# Create default folder for services and sessions.
mkdir -p services
mkdir -p sessions

# Install ROXcomposer-GUI.
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic