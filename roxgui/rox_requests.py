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

#get all running services ?
#def get_services():
#    pass

#start a new service
def start_service(*args):
    pass

#create a new pipeline
def set_pipeline(*args):
    pass