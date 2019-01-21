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

from roxgui.settings import SERVICE_DIR
from web.local_request.rox_response import RoxResponse


def get_local_services() -> RoxResponse:
    """
    Get JSON data of all locally stored services.
    :return: RoxResponse instance containing a list of tuples
        mapping each service name to its corresponding JSON data.
    """
    local_services = []
    for f in os.scandir(SERVICE_DIR):
        if f.is_file() and f.name.endswith(".json"):
            fd = open(os.path.join(SERVICE_DIR, f.name), 'r')
            service_name = f.name[:-5]
            service_json = json.load(fd)
            local_services.append([service_name, service_json])
            fd.close()
    res = RoxResponse(True)
    res.data = local_services
    return res
