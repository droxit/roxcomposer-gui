#!/bin/bash
#
# encoding: utf-8
#
# Install ROXcomposer and its GUI.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

# TODO: Install ROXcomposer-Backend.

# Install Python dependencies.
sudo apt install python3 python3-pip
pip3 install -r requirements.txt

# Install ROXcomposer-GUI.
cd roxgui
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic