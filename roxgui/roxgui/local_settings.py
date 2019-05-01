# encoding: utf-8
#
# Local user-specific settings.
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU General Public License as published by |
# | the Free Software Foundation, either version 3 of the License, or    |
# | (at your option) any later version.                                  |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU General Public License           |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|
#

import configparser
import logging

from web.local_request.rox_response import RoxResponse

# Logging.
# ========
logger = logging.getLogger(__name__)

# Constants.
LOCAL_SETTINGS_FILE_NAME = "config.ini"
SERVICE_DIR = "service_dir"
SESSION_DIR = "session_dir"
ROX_CONNECTOR_IP = "rox_connector_ip"
ROX_CONNECTOR_PORT = "rox_connector_port"

# Local settings.
LOCAL_SETTINGS = dict()


def _write_local_settings_param(key: str, value: str) -> bool:
    """
    Validate and write given key-value pair to local settings.
    :param key: str - Parameter key.
    :param value: str - Parameter value.
    :return: bool - True if parameter could be written and False otherwise.
    """
    if key == SERVICE_DIR:
        # Service file directory.
        LOCAL_SETTINGS[SERVICE_DIR] = value
        return True
    elif key == SESSION_DIR:
        # Session file directory.
        LOCAL_SETTINGS[SESSION_DIR] = value
        return True
    elif key == ROX_CONNECTOR_IP:
        # ROXconnector IP.
        LOCAL_SETTINGS[ROX_CONNECTOR_IP] = value
        return True
    elif key == ROX_CONNECTOR_PORT:
        # ROXconnector port.
        LOCAL_SETTINGS[ROX_CONNECTOR_PORT] = value
        return True
    else:
        # Invalid parameter.
        return False


def update_local_settings(new_settings: dict) -> bool:
    """
    Validate and update given parameters in local settings.
    :param new_settings: dict - Dictionary mapping
        parameter key to its value.
    :return: bool - True if all parameters could be updated and False otherwise.
    """
    # Read settings from config.ini file.
    config = configparser.ConfigParser()
    config.read(LOCAL_SETTINGS_FILE_NAME)

    # Update parameters.
    success = True
    for key, value in new_settings.items():
        res = _write_local_settings_param(key, value)
        if res:
            config.set("Default", key, value)
        else:
            success = False
    if success:
        with open(LOCAL_SETTINGS_FILE_NAME, 'w') as fd:
            config.write(fd)
    return success


def read_local_settings() -> RoxResponse:
    """
    Read local settings specified in config.ini file.
    :return: bool - True if local settings could be read and False otherwise.
    """
    # Store local settings.
    new_settings = dict()

    # Read settings from config.ini file.
    config = configparser.ConfigParser()
    config.read(LOCAL_SETTINGS_FILE_NAME)

    # Get service file directory.
    service_dir = config.get("Default", SERVICE_DIR, fallback=None)
    if service_dir is None:
        # Service file directory is not specified.
        err = 'Specify service file directory ("{}") in config.ini file.'.format(SERVICE_DIR)
        logger.error(err)
        return RoxResponse(False, err)
    else:
        # Service file directory is specified.
        new_settings[SERVICE_DIR] = service_dir

    # Get session file directory.
    session_dir = config.get("Default", SESSION_DIR, fallback=None)
    if session_dir is None:
        # Session file directory is not specified.
        err = 'Specify session file directory ("{}") in config.ini file.'.format(SESSION_DIR)
        logger.error(err)
        return RoxResponse(False, err)
    else:
        # Session file directory is specified.
        new_settings[SESSION_DIR] = session_dir

    # Get ROXconnector IP.
    rox_connector_ip = config.get("Default", ROX_CONNECTOR_IP, fallback=None)
    if rox_connector_ip is None:
        # ROXconnector IP is not specified.
        err = 'Specify ROXconnector IP ("{}") in config.ini file.'.format(ROX_CONNECTOR_IP)
        logger.error(err)
        return RoxResponse(False, err)
    else:
        # ROXconnector IP is specified.
        new_settings[ROX_CONNECTOR_IP] = rox_connector_ip

    # Get ROXconnector port.
    rox_connector_port = config.get("Default", ROX_CONNECTOR_PORT, fallback=None)
    if rox_connector_port is None:
        # ROXconnector port is not specified.
        err = 'Specify ROXconnector port ("{}") in config.ini file.'.format(ROX_CONNECTOR_PORT)
        logger.error(err)
        return RoxResponse(False, err)
    else:
        # ROXconnector port is specified.
        new_settings[ROX_CONNECTOR_PORT] = rox_connector_port

    for key, value in new_settings.items():
        _write_local_settings_param(key, value)
    return RoxResponse(True, "")
