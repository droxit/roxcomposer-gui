import os

import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from roxgui.local_settings import update_local_settings, ROX_COMPOSER_DIR, ROX_CONNECTOR_IP, ROX_CONNECTOR_PORT
from web.local_request import rox_request
from web.local_request.rox_response import RoxResponse


def check_rox_connector_url(url: str) -> RoxResponse:
    """
    Check if ROXconnector is
    available using specified URL.
    :param url: str - ROXconnector URL.
    :return: bool - True if ROXconnector is available
        using specified URL and False otherwise.
    """
    try:
        requests.get(url)
        return RoxResponse(True, "Pinging successful")
    except requests.exceptions.ConnectionError as e:
        return RoxResponse(False, e)


def check_rox_composer_log_file_path(file_path: str) -> RoxResponse:
    """
    Check if ROXcomposer log file is
    available using specified path.
    :param file_path: str - Path to ROXcomposer log file.
    :return: True if ROXcomposer log file is available
        using specified path and False otherwise.
    """
    is_trace_file = os.path.isfile(file_path)
    if is_trace_file:
        return RoxResponse(True, "Tracefile was found")
    else:
        return RoxResponse(False, "Tracelog file could not be found")


@require_http_methods(["POST"])
def check_rox_settings(request) -> JsonResponse:
    """
    Check if parameters specified
    in config.ini file are valid.
    :param request: HTTP request.
    :return: RoxResponse - Indicate if parameters
        in config.ini file are valid.
    """
    result = dict()
    success = False

    # Check ROXconnector URL.
    url = rox_request.get_rox_connector_url()
    res = check_rox_connector_url(url)
    result["running"] = res
    result["ip"] = res
    result["port"] = res
    if not res:
        success = False

    # Check ROXcomposer directory.
    log_file_path = rox_request.get_rox_composer_log_file_path()
    res = check_rox_composer_log_file_path(log_file_path)
    result["path"] = res
    if not res:
        success = False

    response = RoxResponse(success)
    response.data = result
    return JsonResponse(response.convert_to_json())


@require_http_methods(["POST"])
def update_rox_settings(request):
    """
    Update local settings using parameters specified in given request.
    :param request: HTTP request.
    """
    new_settings = dict()

    # Get updated IP.
    ip = request.POST.get("ip", default=None)
    if ip:
        new_settings[ROX_CONNECTOR_IP] = ip

    # Get updated port.
    port = request.POST.get("port", default=None)
    if port:
        new_settings[ROX_CONNECTOR_PORT] = port

    # Get updated path.
    path = request.POST.get("path", default=None)
    if path:
        new_settings[ROX_COMPOSER_DIR] = path

    result_flag = update_local_settings(new_settings)

    response = RoxResponse(result_flag)
    return JsonResponse(response.convert_to_json())
