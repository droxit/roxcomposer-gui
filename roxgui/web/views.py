"""Configuration of web views."""

import logging

import databaseIO
import rox_requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def main(request):
    """Main page."""
    databaseIO.update_service_db()
    service_name_list = rox_requests.get_service_list()
    context = {"service_names": service_name_list}
    return render(request, "web/web.html", context)


@require_http_methods(["POST"])
def start_service(request):
    """Start services specified in POST request's metadata."""
    # Get list of specified service names.
    service_name_list = request.POST.getlist("service_names")
    # Get list of corresponding JSON dictionaries.
    service_json_list = rox_requests.get_service_jsons(service_name_list)
    # service_json = json.load(Service.objects.get(name=service_name).service.service_json)
    # Start services.
    started_services_json_list = rox_requests.start_services(service_json_list)
    if started_services_json_list:

        return HttpResponse("Service could not be started.")
    else:
        # No services could be started.
        return HttpResponse("Services could not be started.")
