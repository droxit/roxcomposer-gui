#!/usr/bin/env python3
#
# rox_requests.py
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#
# Communication with the ROXconnector
#

import json
import logging
import web.databaseIO

import requests
from user_settings import ROX_DIR, ROX_URL

logger = logging.getLogger(__name__)

# get path to composer folder, url
roxconnector = ROX_URL
rox_dir = ROX_DIR



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

    header = {"Content-Type": "application/json"}
    url = "http://{}/start_service".format(roxconnector)

    try:
        r = requests.post(url, json=service_json, headers=header)
    except requests.exceptions.ConnectionError as e:
        logging.error("No connection to server.\n{}".format(e))
        return False
    if r.status_code != 200:
        logging.error("Service could not be started: Error code {}.\n{}".format(r.status_code, r.text))
        return False
    else:
        return True


def start_services(service_json_list: list) -> bool:
    """
    Start all services defined by given list of JSON dictionaries.
    :param service_json_list: List of JSON dictionaries defining multiple services.
    :return: True if all services could be started and False otherwise.
    """
    if len(service_json_list) < 1:
        # Service list is empty and therefore invalid.
        return False

    all_started = True
    for service_json in service_json_list:
        result = start_service(service_json)
        if all_started and not result:
            all_started = False
    return all_started


def shutdown_service(*args):
    if len(args) != 1:
        return 'ERROR: exactly one service needs to be specified for shutdown'

    service = args[0]
    d = {'name': service}
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post('http://{}/shutdown_service'.format(roxconnector), json=d, headers=headers)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)

    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)


def get_running_services():
    """get all registered services (as strings)"""
    try:
        r = requests.get('http://{}/services'.format(roxconnector))
    except requests.exceptions.ConnectionError as e:
        logging.error("ERROR: no connection to server - {}".format(e) )
        return ""

    if r.status_code == 200:
        return r.text
    else:
        logging.error('ERROR: {} - {}'.format(r.status_code, r.text))
        return ""


#TODO
def set_pipeline(pipename, services):
    """create a new pipeline with the specified services, where the order is important"""

    if len(args) < 2:
        return 'ERROR: a pipeline name and at least one service must be specified'
    pipename = args[0]
    services = args[1:]
    d = {'name': pipename, 'services': services}
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post('http://{}/set_pipeline'.format(roxconnector), data=json.dumps(d), headers=headers)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)


#TODO
# get registered pipelines
def get_pipelines(*args):
    r = requests.get('http://{}/pipelines'.format(roxconnector))
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)
