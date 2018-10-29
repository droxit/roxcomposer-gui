"""Configuration of web views."""

import rox_requests
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def main(request):
    """Main page."""
    service_name_list = rox_requests.get_service_list()
    context = {"service_names": service_name_list}
    return render(request, "web/web.html", context)


@require_http_methods(["POST"])
def start_service(request):
    """Start services with post request."""
    service_name = request.POST["services"]
    service_json = rox_requests.get_service_json(service_name)
    rox_requests.start_service(service_json)
