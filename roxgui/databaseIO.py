#!/usr/bin/env python3
#
# databaseIO.py
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#
# Communication with database, such as storing running and
# available services, and registered or saved pipelines.
#

import json
import logging

import filesystemIO
from web.models import Service


def update_service_db():
    """checks the SERVICE_DIR for new services and adds them to the DB"""
    services = filesystemIO.get_service_list()
    for service in services:
        try:
            Service.objects.get(name=service)
        except Service.DoesNotExist:
            service_json = json.dumps(serviceIO.get_service_json(service))
            s = Service(name=service, service_json=service_json)
            s.save()
            logging.info("service saved: " + str(service))


def get_service_jsonf(service_name):
    """get a service json by name out of db"""
    try:
        s = Service.objects.get(name=service_name).service_json
        return json.load(s)
    except Service.MultipleObjectsReturned:
        logging.error("Service name is not unique: " + service_name)
    except Service.DoesNotExist:
        logging.error("Service does not exist: " + service_name)
