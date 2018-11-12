# encoding: utf-8
#
# Communication with database to store and retrieve services and pipelines.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

import json
import logging

import filesystemIO
from web.models import Service


def update_service_db():
    """checks the SERVICE_DIR for new services and adds them to the DB"""
    services = filesystemIO.get_json_available_services()
    for service in services:
        try:
            Service.objects.get(name=service)
        except Service.DoesNotExist:
            service_json = json.dumps(serviceIO.get_service_json(service))
            s = Service(name=service, service_json=service_json)
            s.save()
            logging.info("service saved: " + str(service))


def get_service_json(service_name):
    """get a service json by name out of db"""
    try:
        s = Service.objects.get(name=service_name).service_json
        return json.load(s)
    except Service.MultipleObjectsReturned:
        logging.error("Service name is not unique: " + service_name)
    except Service.DoesNotExist:
        logging.error("Service does not exist: " + service_name)


def get_service_jsons(service_names: list) -> list:
    """
    Get the jsons of specified services out of the database
    :param service_names: list of service names (strings)
    :return: list of jsons for each service
    """
    service_jsons = []
    for service in service_names:
        service_json = get_service_json(service)
        service_jsons.append(service_json)

    return service_jsons
