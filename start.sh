#!/bin/bash

# Store initial working directory.
INITIAL_DIR=$PWD

# Start ROXcomposer-Backend.
cd ../roxcomposer/build/roxcomposer-demo-0.4.0
./start_server.sh &

# Leave server some time to start.
sleep 2

# Start ROXcomposer-GUI.
cd $INITIAL_DIR/roxgui
python3 manage.py runserver