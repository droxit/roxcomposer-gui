#!/bin/bash
#
# encoding: utf-8
#
# Start ROXcomposer and its GUI.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

# Store initial working directory.
INITIAL_DIR=$PWD

# Start ROXcomposer-Backend.
cd ../roxcomposer/build/roxcomposer-demo-0.4.0
./start_server.sh &

# Leave server some time to start.
sleep 2

# Start ROXcomposer-GUI.
cd $INITIAL_DIR/roxgui
./manage.py runserver