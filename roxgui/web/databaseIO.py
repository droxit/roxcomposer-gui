#!/usr/bin/env python3
#
# databaseIO.py
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#
# Communication with the Database, such as storing running and available services,
# and registered or saved pipelines
#

import json
import logging
import serviceIO
from models import Service



def update_service_db():
    """checks the SERVICE_DIR for new services and adds them to the DB"""
    services = rox_requests.get_service_list()
    for service in services:
        try:
            Service.objects.get(name=service)
        except Service.DoesNotExist:
            service_json = json.dumps(serviceIO.get_service_json(service))
            s = Service(name=service, service_json=service_json)
            s.save()
            logging.info("service saved: "+ str(service))