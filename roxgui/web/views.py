"""Configuration of web views."""

import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

import databaseIO
import filesystemIO
import rox_requests

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def main(request):
    """Main page."""
    databaseIO.update_service_db()
    all_service_name_list = filesystemIO.get_service_list()  # TODO: pull from DB
    running_service_name_list =
    context = {"service_names": all_service_name_list}
    return render(request, "web/web.html", context)


@require_http_methods(["POST"])
def start_service(request):
    """Start services specified in POST request's metadata."""
    # Get list of specified service names.
    service_name_list = request.POST.getlist("service_names")
    # Get list of corresponding JSON dictionaries.
    service_json_list = filesystemIO.get_service_jsons_from_filesystem(service_name_list)  # TODO: pull from DB
    # Start services and get list of JSON dictionaries
    # corresponding to all services which could be started.
    started_services_json_list = rox_requests.start_services(service_json_list)
    if started_services_json_list:
        # At least one service could be started.
        started_service_name_list = []
        for started_service in started_services_json_list:
            started_service_name_list.append(started_service["params"]["name"])
            logger.warning(started_service)
        started_services_name_string = ', '.join(started_service_name_list)
        return HttpResponse("Start services: {}".format(started_services_name_string))
    else:
        # No services could be started.
        return HttpResponse("Services could not be started.")


@require_http_methods(["POST"])
def stop_service(request):
    pass
