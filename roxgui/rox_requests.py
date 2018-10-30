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

#Log settings
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
def post_to_pipeline(*args): #TODO
    pass

def get_msg_history(): #TODO
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


def get_running_services() -> list:
    """
    get a list of all registered services (as strings)
    :returns: list of running services
    """

    try:
        r = requests.get('http://{}/services'.format(rox_connector_url))
    except requests.exceptions.ConnectionError as e:
        logging.error("ERROR: no connection to server - {}".format(e))
        return []
    except Exception as e:
        logging.error("ERROR: {}".format(e))

    if r.status_code == 200:
        services =  list(r.json().keys())
        logging.info('currently running services: ' + str(services))
        return services
    else:
        logging.error('ERROR: {} - {}'.format(r.status_code, r.text))
        return []


def set_pipeline(pipename : str, services : list) -> bool:
    """
    create a new pipeline with the specified services, where the order is important
    :param pipename: Name of the Pipeline
    :param services: a list of service names (string) that should be added to the pipeline
    :returns: True if pipeline was sent
    """

    d = {'name': pipename, 'services': services}
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post('http://{}/set_pipeline'.format(rox_connector_url), data=json.dumps(d), headers=headers)
    except requests.exceptions.ConnectionError as e:
        logging.error("ERROR: no connection to server - {}".format(e))
        return False
    if r.status_code == 200:
        logging.info("Pipeline sent, Response: " + r.text)
        return True
    else:
        logging.error('ERROR: {} - {}'.format(r.status_code, r.text))
        return False

def remove_pipeline(): #TODO
    pass

def get_pipelines() -> list:
    """
    get the names of all registered pipelines
    :returns: list of pipeline names
    """
    try:
        r = requests.get('http://{}/pipelines'.format(roxconnector))
    except requests.exceptions.ConnectionError as e:
        logging.error("ERROR: no connection to server - {}".format(e))
        return []

    if r.status_code == 200:
        pipelines = list(r.json().keys())
        logging.info("Currently registered pipelines: "+ str(pipelines))
        return pipelines
    else:
        logging.error('ERROR: {} - {}'.format(r.status_code, r.text))
        return []

def dump_everything(): #TODO
    pass

def watch_services(): #TODO
    pass

def unwatch_services(): #TODO
    pass

def watch_pipelines(): #TODO
    pass

def unwatch_pipelines(): #TODO
    pass

def watch_all(): #TODO
    pass

def reset_watchers(): #TODO
    pass

def get_service_logs(): #TODO
    pass

def load_and_start_pipeline(): #TODO
    pass
