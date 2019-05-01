# encoding: utf-8
#
# Define HTTP responses with JSON data concerning services.
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU General Public License as published by |
# | the Free Software Foundation, either version 3 of the License, or    |
# | (at your option) any later version.                                  |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU General Public License           |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|
#

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from web.local_request import file_request, rox_request
from web.views.json_views import _create_json_context
import json


@require_http_methods(["POST"])
def get_services(request):
    """get a list of all available services and their information"""
    # Get JSON data of local services.
    result = file_request.get_local_services()
    return JsonResponse(result.convert_to_json())


@require_http_methods(["POST"])
def get_running_services(request):
    """get a list of all running services and their information"""
    # Get JSON data of local services.
    result = rox_request.get_running_services()
    return JsonResponse(result.convert_to_json())


@require_http_methods(["POST"])
def get_service_info(request):
    """
    Returns the info of services in a dictionary (their parameters etc.)
    :param request: contains a list "services" with the names of all services that the info should be retrieved of
    :return: a JsonResponse context with key value pairs,
            where the key is the service name and value the corresponding service info
    """
    services = json.loads(request.POST.get("services", default=""))
    result = file_request.get_local_services()

    service_dict = {}

    for entry in result.data:
        service_dict[entry] = result.data[entry]
    info = {}
    for service in services:
        if service["service"] in service_dict:
            info[service["service"]] = service_dict[service["service"]]

    return JsonResponse(info)


@require_http_methods(["POST"])
def get_service_info_specific_service(request):
    """
    Returns the info of services in a dictionary (their parameters etc.)
    :param request: contains a list "services" with the names of all services that the info should be retrieved of
    :return: a JsonResponse context with key value pairs,
            where the key is the a service parameter name and value the corresponding parameter value
    """
    service = request.POST.get("service", default="")
    result = file_request.get_local_services()

    info = {}

    for entry in result.data:
        if service == entry:
            info = result.data[entry]

    return JsonResponse(info)


@require_http_methods(["POST"])
def check_running(request):
    """
    For a specified list of services returns which of those are running
    :param request: contains list of service names
    :return: dictionary with service names as  keys and boolean as value,
            the boolean indicates if the service is running.
    """
    result = rox_request.get_running_services()
    running_services = result.data
    services = request.POST.getlist("services[]", default=[])

    running = {}
    for service in services:
        service_is_running = False
        if service in running_services:
            service_is_running = True
        running[service] = service_is_running
    context = _create_json_context(running)
    return JsonResponse(context)


@require_http_methods(["POST"])
def start_services(request):
    """Start services specified in POST request's metadata."""
    # Get list of service names which should be started.
    service_name_list = request.POST.getlist("services[]", default=[])
    # Get list of corresponding JSON dictionaries.
    res = file_request.convert_to_service_json_list(service_name_list)
    service_json_list = res.data
    # Start specified services and get list of JSON dictionaries
    # corresponding to all services which could not be started.
    result = rox_request.start_services(service_json_list)
    return JsonResponse(result.convert_to_json())


@require_http_methods(["POST"])
def stop_services(request):
    """Stop services specified in POST request's metadata."""
    # Get list of service names which should be stopped.
    services = request.POST.getlist("services[]", default=[])
    # Stop specified services and get list of names
    # corresponding to all services which could not be stopped.
    res = rox_request.shutdown_services(services)
    if res.success:
        # All services could be stopped.
        return JsonResponse(res.convert_to_json())
    else:
        # Some services could not be stopped.
        if not res.error_data:
            # No services were specified.
            return JsonResponse(res.convert_to_json())
        else:
            # Some services were specified but could not be stopped.
            # services_not_stopped = ", ".join(res.error_data)
            return JsonResponse(res.convert_to_json())


@require_http_methods(["POST"])
def delete_service(request):
    """ Delete a service from file system """
    # Get the service name of the service that should be deleted.
    service = request.POST.get("service", default="")
    res = file_request.delete_service(service)
    return JsonResponse(res.convert_to_json())


@require_http_methods(["POST"])
def create_service(request):
    """Create service with specified parameters."""
    res = rox_request.create_service(
        ip=request.POST.get("ip"),
        port=request.POST.get("port"),
        name=request.POST.get("name"),
        class_path=request.POST.get("classpath"),
        path=request.POST.get("path"),
        optional_param_keys=request.POST.getlist("optional_param_keys[]", default=[]),
        optional_param_values=request.POST.getlist("optional_param_values[]", default=[])
    )
    return JsonResponse(res.convert_to_json())
