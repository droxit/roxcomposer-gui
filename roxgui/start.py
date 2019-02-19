#!/usr/bin/python3
#
# encoding: utf-8
#
# Start ROXcomposer and its GUI.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

import configparser
import os
import shlex
import signal
import subprocess

from roxgui.local_settings import LOCAL_SETTINGS_FILE_NAME, ROX_COMPOSER_DIR
from web.local_request.rox_request import RELATIVE_ROX_COMPOSER_BUILD_PATH


# Custom signal handler.
def handler(signum, frame):
    if backend_server is not None:
        backend_server.kill()


# Enable custom signal handler.
signal.signal(signal.SIGINT, handler)

# Define ROXcomposer start script.
START_SCRIPT_FILE_NAME = "start_server.sh"

if __name__ == "__main__":
    # Store process ID of ROXcomposer backend server.
    backend_server = None

    # Read ROXcomposer directory from config.ini file.
    config = configparser.ConfigParser()
    config.read(LOCAL_SETTINGS_FILE_NAME)
    rox_composer_dir = config.get("Default", ROX_COMPOSER_DIR, fallback=None)
    if rox_composer_dir is None:
        # ROXcomposer directory is not specified.
        err = 'Specify ROXcomposer directory ("{}") in config.ini file.'.format(ROX_COMPOSER_DIR)
        print(err)
        exit(1)

    # Store current path.
    initial_path = os.getcwd()

    # Move to build directory.
    build_path = os.path.join(rox_composer_dir, RELATIVE_ROX_COMPOSER_BUILD_PATH)
    os.chdir(build_path)

    # Start ROXcomposer backend server.
    start_script_path = os.path.join(".", START_SCRIPT_FILE_NAME)
    start_script_command = shlex.split(start_script_path)
    try:
        backend_server = subprocess.Popen(start_script_command)
    except OSError as err:
        print(err)
        exit(1)

    # Move back to initial directory.
    os.chdir(initial_path)

    # Start ROXcomposer frontend server.
    start_script_command = shlex.split("./manage.py runserver")
    result = subprocess.run(start_script_command)
    try:
        result.check_returncode()
    except subprocess.CalledProcessError as err:
        print(err)
        exit(1)
