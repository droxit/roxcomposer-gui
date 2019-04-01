# encoding: utf-8
#
# Communication with filesystem to retrieve locally stored data.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

import json
import os

from roxgui.local_settings import LOCAL_SETTINGS, SERVICE_DIR
from web.local_request.rox_response import RoxResponse


def get_local_services() -> RoxResponse:
    """
    Get locally stored services and provide
    them as dictionary mapping service name to
    its JSON instance. Provide list of invalid
    services as RoxResponse's error data parameter.
    :return: RoxResponse instance containing a
        dictionary mapping each service name
        to its corresponding JSON instance Provide
        list of invalid services as error data parameter.
    """
    valid_services = {}
    invalid_services = []
    success = True

    for f in os.scandir(LOCAL_SETTINGS[SERVICE_DIR]):
        if f.is_file() and f.name.endswith(".json"):
            fd = None
            service_name = None
            try:
                fd = open(os.path.join(LOCAL_SETTINGS[SERVICE_DIR], f.name), 'r')
                service_name = f.name[:-5]
                service_json = json.load(fd)
                valid_services[service_name] = service_json
            except (OSError, json.decoder.JSONDecodeError):
                success = False
                if service_name:
                    invalid_services.append(service_name)
            finally:
                if fd:
                    fd.close()

    res = RoxResponse(success)
    res.data = valid_services
    res.error_data = invalid_services
    return res


def delete_service(name: str) -> RoxResponse:
    """
    Delete a service from file system.
    :param name: Service name
    :return: RoxResponse with information whether deleting worked
    """
    f_name = os.path.join(LOCAL_SETTINGS[SERVICE_DIR], name + ".json")
    try:
        os.remove(f_name)
        res = RoxResponse(True)
    except FileNotFoundError:
        res = RoxResponse(False, "File not found.")
    except PermissionError:
        res = RoxResponse(False, "No permission to delete file.")

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
        fd = open(os.path.join(LOCAL_SETTINGS[SERVICE_DIR], name_with_ext))
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
