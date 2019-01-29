# encoding: utf-8
#
# Define HTTP responses with JSON data concerning services.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from web.local_request import file_request, rox_request
from web.views.json_views import _create_json_context


@require_http_methods(["POST"])
def get_services(request):
    """get a list of all available services and their information"""
    # Get JSON data of local services.
    result = file_request.get_local_services()
    return JsonResponse(result.data)

@require_http_methods(["POST"])
def get_service_info(request):
    """
    Returns the info of services in a dictionary (their parameters etc.)
    :param request: contains a list "services" with the names of all services that the info should be retrieved of
    :return: a JsonResponse context with key value pairs, where the key is the service name and value the corresponding service info
    """
    services = request.POST.getlist("services[]", default=[])
    result = file_request.get_local_services()

    service_dict = {}

    for entry in result.data:
        service_dict[entry[0]] = entry[1]
    info = {}
    for service in services:
        if service in service_dict:
            info[service] = service_dict[service]

    context = _create_json_context(info)
    return JsonResponse(context)

@require_http_methods(["POST"])
def check_running(request):
    """
    For a specified list of services returns which of those are running
    :param request: contains list of service names
    :return: dictionary with service names as  keys and boolean as value, the boolean indicates if the service is running.
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
    if result.success:
        # All services could be started.
        return JsonResponse(res.convert_to_json())
    else:
        # Some services could not be started.
        if not result.error_data:
            # No services were specified.
            return JsonResponse(res.convert_to_json())
        else:
            # Some services were specified but could not be started.
            services_not_started = ", ".join(result.error_data)
            return JsonResponse(res.convert_to_json())


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
            #services_not_stopped = ", ".join(res.error_data)
            return JsonResponse(res.convert_to_json())
