# encoding: utf-8
#
# Communication with local filesystem to retrieve stored services.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

import json
import logging
import os

import rox_requests
from user_settings import SERVICES_DIR

services_dir = SERVICES_DIR


def get_json_available_services() -> dict:
    """
    Get JSON data of all available services.
    :return: Dictionary concerning all available services
    (key: unique service name, value: corresponding JSON data).
    May be empty in case of an error.
    """
    available_services = {}
    for f in os.scandir(services_dir):
        if f.is_file() and f.name.endswith('.json'):
            if f.name[:-5] in rox_requests.FORBIDDEN_SERVICES:
                continue
            service_file = open(os.path.join(services_dir, f.name), 'r')
            service_args = json.load(service_file)
            available_services[f.name[:-5]] = service_args
            service_file.close()
    return available_services


def get_name_available_services() -> list:
    """
    Get names of all available services.
    :return: List of names concerning all available services.
    May be empty in case of an error.
    """
    available_services = []
    for f in os.scandir(services_dir):
        if f.is_file() and f.name.endswith('.json'):
            if f.name[:-5] in rox_requests.FORBIDDEN_SERVICES:
                continue
            available_services.append(f.name[:-5])
    return available_services


def get_service_json_from_filesystem(service_name: str) -> dict:
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


def get_service_jsons_from_filesystem(service_name_list: list) -> list:
    """
    Convert list of service names to corresponding list of JSON dictionaries.
    :param service_name_list: List of service names.
    :return: Corresponding list of JSON dictionaries which may be empty in case of an error.
    """
    service_jsons = []
    for name in service_name_list:
        json_data = get_service_json_from_filesystem(name)
        if json_data is not None:
            service_jsons.append(json_data)
    return service_jsons
