#!/usr/bin/env python3
#
# rox_requests.py
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#
# Communication with ROXconnector.
#

import json
import logging

import requests

from user_settings import ROX_DIR, ROX_URL

logger = logging.getLogger(__name__)
logging.basicConfig(filename="test.log", filemode='w', level=logging.INFO)

# Connection details for ROXconnector.
# ====================================

# URL to ROXconnector.
rox_connector_url = ROX_URL

# Path to ROXcomposer project.
rox_composer_dir = ROX_DIR

# Constants.
# ==========

# Header for JSON data.
JSON_HEADER = {"Content-Type": "application/json"}

# Error message for connection error.
MSG_CONNECTION_ERROR = "No connection to server."


# post data to pipeline
def post_to_pipeline(*args):
    pass


def start_service(service_json: dict) -> bool:
    """
    Start service defined by given JSON dictionary.
    :param service_json: JSON dictionary defining service.
    :return: True if service could be started and False otherwise.
    """
    if not service_json:
        # JSON data is empty and therefore invalid.
        return False

    url = "http://{}/start_service".format(rox_connector_url)

    try:
        r = requests.post(url, json=service_json, headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        logging.error("{}\n{}".format(MSG_CONNECTION_ERROR, err))
        return False
    if r.status_code != 200:
        logging.error("Service could not be started. Error code {}.\n{}".format(r.status_code, r.text))
        return False
    else:
        return True


def start_services(service_json_list: list) -> list:
    """
    Start all services defined by given list of JSON dictionaries.
    :param service_json_list: List of JSON dictionaries defining multiple services.
    :return: List of JSON dictionaries representing all services which could be started.
    """
    started_services_json_list = []
    if len(service_json_list) < 1:
        # Service list is empty and therefore invalid.
        return started_services_json_list

    for service_json in service_json_list:
        result = start_service(service_json)
        if result:
            started_services_json_list.append(service_json)
    return started_services_json_list


def shutdown_service(service_json: dict) -> bool:
    """
    Stop service defined by given JSON dictionary.
    :param service_json: JSON dictionary defining service.
    :return: True if service could be stopped and False otherwise.
    """
    if not service_json:
        # JSON data is empty and therefore invalid.
        return False

    url = "http://{}/shutdown_service".format(rox_connector_url)
    data = {'name': service_json}

    try:
        r = requests.post(url, json=data, headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        logger.error("{}\n{}".format(MSG_CONNECTION_ERROR, err))
        return False
    if r.status_code != 200:
        logging.error("Service could not be stopped. Error code {}.\n{}".format(r.status_code, r.text))
        return False
    else:
        return True


def shutdown_services(service_json_list: list) -> list:
    """
    Stop all services defined by given list of JSON dictionaries.
    :param service_json_list: List of JSON dictionaries defining multiple services.
    :return: List of JSON dictionaries representing all services which could be stopped.
    """
    stopped_services_json_list = []
    if len(service_json_list) < 1:
        # Service list is empty and therefore invalid.
        return stopped_services_json_list

    for service_json in service_json_list:
        result = shutdown_service(service_json)
        if result:
            stopped_services_json_list.append(service_json)
    return stopped_services_json_list


def get_running_services():
    """get a list of all registered services (as strings)"""
    try:
        r = requests.get('http://{}/services'.format(rox_connector_url))
    except requests.exceptions.ConnectionError as e:
        logging.error("ERROR: no connection to server - {}".format(e))
        return []
    except Exception as e:
        logging.error("ERROR: {}".format(e))

    if r.status_code == 200:
        #logging.info('currently running services: ' + r.text + '\n')
        services =  list(r.json().keys())
        logging.info('currently running services: ' + str(services))
        return services
    else:
        logging.error('ERROR: {} - {}'.format(r.status_code, r.text))
        return []


# TODO
def set_pipeline(pipename, services):
    """create a new pipeline with the specified services, where the order is important"""

    if len(args) < 2:
        return 'ERROR: a pipeline name and at least one service must be specified'
    pipename = args[0]
    services = args[1:]
    d = {'name': pipename, 'services': services}
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post('http://{}/set_pipeline'.format(rox_connector_url), data=json.dumps(d), headers=headers)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)


# TODO
# get registered pipelines
def get_pipelines(*args):
    r = requests.get('http://{}/pipelines'.format(rox_connector_url))
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)
