#!/usr/bin/env python3
#
# rox_requests.py
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

import json
import logging
import os

import requests
from user_settings import ROX_DIR, SERVICES_DIR, ROX_URL

logger = logging.getLogger(__name__)

# get path to composer folder, url, services directory
services_dir = SERVICES_DIR
roxconnector = ROX_URL
rox_dir = ROX_DIR


# get a list of all available services in the services directory
# key: unique service name, value: its JSON data
def get_service_list():
    available_services = {}
    for f in os.scandir(services_dir):
        if f.is_file() and f.name.endswith('.json'):
            service_file = open(os.path.join(services_dir, f.name), 'r')
            service_args = json.load(service_file)
            available_services[f.name[:-5]] = service_args
            service_file.close()
    return available_services


# get the names of available services
def get_service_names():
    available_services = []
    for f in os.scandir(services_dir):
        if f.is_file() and f.name.endswith('.json'):
            available_services.append(f.name[:-5])
    return available_services

# convert service name to corresponding JSON data
def get_service_json(service_name):
    try:
        service_name = service_name + ".json"
        service_file = open(os.path.join(services_dir, service_name))
        service_json = json.load(service_file)
    except Exception as e:
        return 'ERROR unable to load service {} - {}'.format(service_name, e)
    finally:
        service_file.close()
    return service_json


def get_service_jsons(service_names: list) -> list:
    """
    Convert service names to corresponding JSON data.
    :param service_name: List of service names.
    :return: Corresponding list of JSON data which may be empty when no JSON strings could be received.
    """
    service_jsons = []
    for name in service_names:
        name_with_ext = name + ".json"
        try:
            service_file = open(os.path.join(services_dir, name_with_ext))
            json_data = json.load(service_file)
            service_jsons.append(json_data)
        except OSError:
            logging.error("Could not open JSON file for service {}.".format(name))
        except json.JSONDecodeError:
            logging.error("JSON data for service {} is broken.".format(name))

        finally:
            service_file.close()
    return service_jsons


# post data to pipeline
def post_to_pipeline(*args):
    pass


def start_service(*args: str) -> bool:
    """
    Start services defined by given JSON strings.
    :param args: JSON strings.
    :return: True if service could be started and False otherwise.
    """
    if len(args) < 1:
        return False

    header = {"Content-Type": "application/json"}
    url = "http://{}/start_service".format(roxconnector)

    for service_json in args:
        try:
            r = requests.post(url, json=service_json, headers=header)
        except requests.exceptions.ConnectionError as e:
            logging.error("No connection to server.\n{}".format(e))
            return False
        if r.status_code != 200:
            logging.error("Service could not be started: Error code {}.\n{}".format(r.status_code, r.text))
    return True


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


# get all registered services
def get_services():
    try:
        r = requests.get('http://{}/services'.format(roxconnector))
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)

    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)


# create a new pipeline
def set_pipeline(pipename, services):
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


# get registered pipelines
def get_pipelines(*args):
    r = requests.get('http://{}/pipelines'.format(roxconnector))
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)
