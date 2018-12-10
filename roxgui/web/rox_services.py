import datetime
import json
import logging
import os

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods


import filesystemIO
import rox_request

from web import views

@require_http_methods(["POST"])
def create_service(request):
    """Create service specified in POST request's metadata."""
    # Get IP address.
    ip = request.POST.get("ip")
    # Check if given IP is valid.
    ip_parts = ip.split('.')
    for part in ip_parts:
        part = int(part)
        if not (0 <= part <= 255):
            messages.error(request, "Invalid IP address.")
            return redirect(views.main)
    # Get port number.
    port = int(request.POST.get("port"))
    # Get service name.
    name = request.POST.get("name")
    # Get classpath.
    class_path = request.POST.get("class_path")
    # Get path to output file.
    output_file_path = request.POST.get("output_file_path", "")
    if output_file_path:
        # Output file is specified. It does not
        # need to exist yet, but its directory should.
        if os.path.isdir(os.path.dirname(output_file_path)):
            # Output file path is valid.
            res = rox_request.create_service(ip, port, name, class_path, output_file_path)
        else:
            # Redirect with error.
            messages.error(request, "Path to output file invalid.")
            return redirect(views.main)
    else:
        # Output file is not specified.
        res = rox_request.create_service(ip, port, name, class_path)

    if res.success:
        messages.success(request, "Service created successfully.")
    else:
        messages.error(request, "Service could not be created.")
    return redirect(views.main)


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
        return redirect(views.main)
    else:
        # Some services could not be started.
        if not result.error_data:
            # No services were specified.
            messages.error(request, result.message)
            return redirect(views.main)
        else:
            # Some services were specified but could not be started.
            services_not_started = ", ".join(result.error_data)
            messages.error(request, "Unable to start service: {}.".format(services_not_started))
            return redirect(views.main)


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
        return redirect(views.main)
    else:
        # Some services could not be stopped.
        if not res.error_data:
            # No services were specified.
            messages.error(request, res.message)
            return redirect(views.main)
        else:
            # Some services were specified but could not be stopped.
            services_not_stopped = ", ".join(res.error_data)
            messages.error(request, "Unable to stop service: {}.".format(services_not_stopped))
            return redirect(views.main)