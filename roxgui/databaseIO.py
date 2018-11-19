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
import rox_request
from rox_response import RoxResponse
from web.models import Service, RoxSession


def update_service_db():
    """checks the SERVICE_DIR for new services and adds them to the DB"""
    res = filesystemIO.get_available_service_jsons()
    services = res.data
    for service in services:
        try:
            Service.objects.get(name=service)
        except Service.DoesNotExist:
            res = filesystemIO.convert_to_service_json(service)
            if res.success:
                service_json = json.dumps(res.data)
                s = Service(name=service, service_json=service_json)
                s.save()
            else:
                logging.error(res.message)


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
        if service[:-5] in rox_request.FORBIDDEN_SERVICES:
            continue
        service_json = get_service_json(service)
        service_jsons.append(service_json)

    return service_jsons


def get_session(session_id: str) -> RoxResponse:
    """
    Get session with specified ROXcomposer ID.
    :param session_id: Session's ROXcomposer ID.
    :return: RoxResponse instance with corresponding session data.
    """
    try:
        s = RoxSession.objects.get(id=session_id)
        services = set(s.services.split(", "))
        sess = {'id': s.id, 'timeout': s.timeout, 'services': services}
        res = RoxResponse(True)
        res.data = sess
        return res
    except RoxSession.DoesNotExist:
        error_msg = "Session {} does not exist.".format(session_id)
        return RoxResponse(False, error_msg)
