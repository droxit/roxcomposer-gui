# encoding: utf-8
#
# Define HTTP responses concerning service handling.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

import filesystemIO
import rox_request


@require_http_methods(["POST"])
def get_services(request):
    # Get JSON data of all available services (excluding forbidden ones).
    file_result = filesystemIO.get_available_service_jsons()
    available_services_json_dict = file_result.data
    # Get JSON data of all running services (excluding forbidden ones).
    rox_result = rox_request.get_running_service_jsons()
    running_services_json_dict = rox_result.data
    # Only consider services which are currently not running as available.
    tmp_dict = {}
    for service_name, service_info in available_services_json_dict.items():
        if service_name not in running_services_json_dict:
            tmp_dict[service_name] = service_info
    available_services_json_dict = tmp_dict
    context = {"available_services": available_services_json_dict,
               "running_services": running_services_json_dict,
               "watch_active": request.session.get('watch_button_active', None)
               }
    return JsonResponse(context)


@require_http_methods(["POST"])
def start_service(request):
    """Start services specified in POST request's metadata."""
    # Get list of service names which should be started.
    service_name_list = request.POST.getlist("available_service_names[]", default=[])
    # Get list of corresponding JSON dictionaries.
    res = filesystemIO.convert_to_service_json_list(service_name_list)
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
            messages.error(request, result.message)
            return JsonResponse(res.convert_to_json())
        else:
            # Some services were specified but could not be started.
            services_not_started = ", ".join(result.error_data)
            messages.error(request, "Unable to start service: {}.".format(services_not_started))
            return JsonResponse(res.convert_to_json())


@require_http_methods(["POST"])
def stop_service(request):
    """Stop services specified in POST request's metadata."""
    # Get list of service names which should be stopped.
    service_name_list = request.POST.getlist("running_service_names[]", default=[])
    # Stop specified services and get list of names
    # corresponding to all services which could not be stopped.
    res = rox_request.shutdown_services(service_name_list)
    if res.success:
        # All services could be stopped.
        return JsonResponse(res.convert_to_json())
    else:
        # Some services could not be stopped.
        if not res.error_data:
            # No services were specified.
            messages.error(request, res.message)
            return JsonResponse(res.convert_to_json())
        else:
            # Some services were specified but could not be stopped.
            services_not_stopped = ", ".join(res.error_data)
            messages.error(request, "Unable to stop service: {}.".format(services_not_stopped))
            return JsonResponse(res.convert_to_json())
