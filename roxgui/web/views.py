"""Configuration of web views."""

import rox_requests
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Service
import json


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
        if Service.objects.filter(name = service).count() == 0:
            service_json = json.dumps(rox_requests.get_service_json(service))
            s = Service(name = service, service_json = service_json)
            s.save()




@require_http_methods(["POST"])
def start_service(request):
    """Start services with post request."""
    service_name = request.POST["services"]
    service_json = rox_requests.get_service_json(service_name)
    rox_requests.start_service(service_json)
