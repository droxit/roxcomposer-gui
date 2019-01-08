# encoding: utf-8
#
# Communication with local filesystem to retrieve stored services.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

import json
import os

from rox_request import FORBIDDEN_SERVICES
from rox_response import RoxResponse
from roxgui.settings import SERVICE_DIR


# File system operations.
# =======================

def get_available_service_jsons() -> RoxResponse:
    """
    Get JSON data of all available services excluding forbidden ones.
    :return: RoxResponse instance containing a dictionary which maps each service name to its corresponding JSON data.
    """
    available_services = {}
    for f in os.scandir(SERVICE_DIR):
        if f.is_file() and f.name.endswith(".json"):
            if f.name[:-5] in FORBIDDEN_SERVICES:
                continue
            service_file = open(os.path.join(SERVICE_DIR, f.name), 'r')
            service_args = json.load(service_file)
            available_services[f.name[:-5]] = service_args
            service_file.close()
    res = RoxResponse(True)
    res.data = available_services
    return res


def convert_to_service_json(service_name: str) -> RoxResponse:
    """
    Convert service name to corresponding JSON dictionary.
    :param service_name: Service name.
    :return: RoxResponse instance containing corresponding JSON dictionary.
    """
    fd = None
    name_with_ext = service_name + ".json"
    try:
        fd = open(os.path.join(SERVICE_DIR, name_with_ext))
        json_data = json.load(fd)
    except OSError:
        error_msg = "Could not open JSON file for service {}.".format(service_name)
        return RoxResponse(False, error_msg)
    except json.JSONDecodeError:
        error_msg = "JSON data for service {} is invalid.".format(service_name)
        return RoxResponse(False, error_msg)
    finally:
        if fd is not None:
            fd.close()
    res = RoxResponse(True)
    res.data = json_data
    return res


def convert_to_service_json_list(service_name_list: list) -> RoxResponse:
    """
    Convert list of service names to corresponding list of JSON dictionaries.
    :param service_name_list: List of service names.
    :return: RoxResponse instance containing a list of corresponding JSON dictionaries. Service
    names which could not be converted to JSON structure are included as error_data attribute.
    """
    valid_service_jsons = []
    invalid_service_names = []
    for name in service_name_list:
        res = convert_to_service_json(name)
        if res.success:
            valid_service_jsons.append(res.data)
        else:
            invalid_service_names.append(name)
    res = RoxResponse(True)
    res.data = valid_service_jsons
    res.error_data = invalid_service_names
    return res
