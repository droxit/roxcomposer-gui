#!/bin/bash

# TODO: Install ROXcomposer-Backend.

# Install Python packages.
sudo apt install python3-pip
pip3 install -r requirements.txt

# Install ROXcomposer-GUI.
cd roxgui
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic