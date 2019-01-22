# encoding: utf-8
#
# Define HTTP responses with JSON data.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from web.local_request import file_request, rox_request



def _create_json_context(data) -> dict:
    """
    Create default context dictionary for JSON responses.
    :param data: Data structure which should be attached.
    :return: Default context dictionary for JSON responses.
    """
    context = {"data": data}
    return context


@require_http_methods(["POST"])
def get_services(request):
    # Get JSON data of local services.
    result = file_request.get_local_services()
    local_services_json_dict = result.data
    # Prepare and return JSON response.
    context = _create_json_context(local_services_json_dict)
    return JsonResponse(context)

@require_http_methods(["POST"])
def check_running(request):
    result = rox_request.get_running_services()
    running_services = result.data
    services = request.POST.getlist("services[]", default=[])

    running = {}
    print(services, running_services)
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



@require_http_methods(["POST"])
def get_pipelines(request):
    # Get JSON data of local pipelines.
    result = rox_request.get_pipelines()
    pipelines_json_dict = result.data
    # Prepare and return JSON response.
    context = _create_json_context(pipelines_json_dict)
    return JsonResponse(context)
