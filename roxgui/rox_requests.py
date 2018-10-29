#! /usr/bin/env python3
#
# commands.py
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

import json
import os
import requests
from user_settings import ROX_DIR, SERVICES_DIR, ROX_URL

#get path to composer folder, url, services directory
services_dir = SERVICES_DIR
roxconnector = ROX_URL
rox_dir = ROX_DIR


#get a list of all available services in the services directory
def get_service_list():
    available_services = {}
    for f in os.scandir(services_dir):
        if f.is_file() and f.name.endswith('.json'):
            service_file = open(os.path.join(services_dir, f.name))
            service_args = json.load(service_file)
            available_services[f.name[:-5]] = service_args
            service_file.close()

    return available_services

#post message to pipeline
def post_to_pipeline(*args):
    pass


#start a new service
def start_service(service_json):
    headers = {'Content-Type': 'application/json'}

    try:
        r = requests.post('http://{}/start_service'.format(roxconnector), json=service_json, headers=headers)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)

#get all registered services
def get_services():
    try:
        r = requests.get('http://{}/services'.format(roxconnector))
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)

    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)

#create a new pipeline
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

#get registered pipelines
def get_pipelines(*args):
    r = requests.get('http://{}/pipelines'.format(roxconnector))
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)

