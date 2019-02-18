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
sudo apt-get install python3 python3-pip
pip3 install -r requirements.txt

# Install ROXcomposer-GUI.
./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic