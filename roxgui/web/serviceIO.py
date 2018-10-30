#!/usr/bin/env python3
#
# serviceIO.py
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#
# Communication with the ROXconnector
#

import rox_requests
import json
import logging
import os
from user_settings import SERVICES_DIR


services_dir = SERVICES_DIR #get path to services directory


def get_service_list():
    """
    get a list of all available services in the services directory
    key: unique service name, value: its JSON data
    """
    available_services = {}
    for f in os.scandir(services_dir):
        if f.is_file() and f.name.endswith('.json'):
            service_file = open(os.path.join(services_dir, f.name), 'r')
            service_args = json.load(service_file)
            available_services[f.name[:-5]] = service_args
            service_file.close()
    return available_services


def get_service_names():
    """get the names of available services in a list (names are unique)"""

    available_services = []
    for f in os.scandir(services_dir):
        if f.is_file() and f.name.endswith('.json'):
            available_services.append(f.name[:-5])
    return available_services


def get_service_json(service_name: str) -> dict:
    """
    Convert service name to corresponding JSON dictionary.
    :param service_name: Service name as string.
    :return: Corresponding JSON dictionary which may be None in case of an error.
    """
    json_data = None
    name_with_ext = service_name + ".json"
    service_file = None
    try:
        service_file = open(os.path.join(services_dir, name_with_ext))
        json_data = json.load(service_file)
    except OSError:
        logging.error("Could not open JSON file for service {}.".format(service_name))
    except json.JSONDecodeError:
        logging.error("JSON data for service {} is broken.".format(service_name))
    finally:
        if service_file is not None:
            service_file.close()
    return json_data


def get_service_jsons(service_name_list: list) -> list:
    """
    Convert service name list to corresponding list of JSON dictionaries.
    :param service_name_list: List of service names.
    :return: Corresponding list of JSON dictionaries which may be empty in case of an error.
    """
    service_jsons = []
    for name in service_name_list:
        json_data = get_service_json(name)
        if json_data is not None:
            service_jsons.append(json_data)
    return service_jsons