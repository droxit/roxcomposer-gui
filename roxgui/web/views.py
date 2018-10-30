"""Configuration of web views."""

import logging

import rox_requests
import databaseIO
import filesystemIO
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def main(request):
    """Main page."""
    databaseIO.update_service_db()
    service_name_list = filesystemIO.get_service_list() #TODO: pull from DB
    context = {"service_names": service_name_list}
    return render(request, "web/web.html", context)


@require_http_methods(["POST"])
def start_service(request):
    """Start services specified in POST request's metadata."""
    # Get list of specified service names.
    service_name_list = request.POST.getlist("service_names")
    # Get list of corresponding JSON dictionaries.
    service_json_list = filesystemIO.get_service_jsons_from_filesystem(service_name_list) #TODO: pull from DB
    # Start services.
    started_services_json_list = rox_requests.start_services(service_json_list)
    if started_services_json_list:

        return HttpResponse("Service could not be started.")
    else:
        # No services could be started.
        return HttpResponse("Services could not be started.")
