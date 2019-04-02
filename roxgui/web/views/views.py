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
        return RoxResponse(False, str(e))


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


@require_http_methods(["GET"])
def check_rox_settings(request) -> JsonResponse:
    """
    Check if parameters specified
    in config.ini file are valid.
    :param request: HTTP request.
    :return: RoxResponse - Indicate if parameters
        in config.ini file are valid.
    """
    return check()


def check() -> JsonResponse:
    """
    Check function that does not require HTTP request. Check if parameters specified
    in config.ini file are valid.
    :return: RoxResponse - Indicate if parameters
        in config.ini file are valid.
    """
    result = dict()
    success = True

    # Check ROXconnector URL.
    url = rox_request.get_rox_connector_url()
    res_url = check_rox_connector_url(url)
    if res_url.success:
        result["running"] = res_url.success
        result["ip_set"] = res_url.success
        result["port_set"] = res_url.success

    domain = url.strip("http://").strip("https://")
    if len(domain.split(":")) > 1:
        port = domain.split(":")[-1]
        ip = domain.split(":")[0]
    else:
        port = domain.split("/")[-1]
        ip = domain.split("/")[0]

    result["ip"] = ip
    result["port"] = port

    # Check ROXcomposer directory.
    rox_path = rox_request.get_file_path()
    log_file_path = rox_request.get_rox_composer_log_file_path()
    res = check_rox_composer_log_file_path(log_file_path)

    # TODO: Actually, the user should not be concerned
    #  with any internal log file. In future releases,
    #  0this will be handled in backend. In this case,
    #  the current config file needs to be adjusted.
    res.success = True

    result["path_set"] = res.success
    result["path"] = rox_path
    if not res.success:
        res.data = result
        return JsonResponse(res.convert_to_json())

    if not res_url.success:
        res_url.data = result
        return JsonResponse(res_url.convert_to_json())

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

    update_local_settings(new_settings)

    return check()
    # response = RoxResponse(result_flag)
    # return JsonResponse(response.convert_to_json())


