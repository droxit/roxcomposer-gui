"""Configuration of web views."""

import json
import logging

import rox_requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Service

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def main(request):
    """Main page."""
    update_service_db()
    service_name_list = rox_requests.get_service_list()
    context = {"service_names": service_name_list}
    return render(request, "web/web.html", context)


def update_service_db():
    """checks the SERVICE_DIR for new services and adds them to the DB"""
    services = rox_requests.get_service_list()
    for service in services:
        try:
            Service.objects.get(name=service)
        except Service.DoesNotExist:
            service_json = json.dumps(rox_requests.get_service_json(service))
            s = Service(name=service, service_json=service_json)
            s.save()


@require_http_methods(["POST"])
def start_service(request):
    """Start services specified in POST request's metadata."""
    # Get list of specified service names.
    service_name = request.POST["service_names"]
    logger.error(type(request))
    logger.error(str(request))
    logger.error(repr(request))
    # return HttpResponse(request)
    # Get list of corresponding JSON dictionaries.
    service_json = rox_requests.get_service_json(service_name)
    # service_json = json.load(Service.objects.get(name=service_name).service.service_json)
    # Start services.
    result = rox_requests.start_service(service_json)
    if result:
        return HttpResponse("Service started.")
    else:
        return HttpResponse("Service could not be started.")
