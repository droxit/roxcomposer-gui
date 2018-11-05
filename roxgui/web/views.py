"""Configuration of web views."""

import logging

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

import databaseIO
import filesystemIO
import rox_requests
from web import views

logger = logging.getLogger(__name__)

# Error message for connection error.
MSG_CONNECTION_ERROR = "No connection to server."


@require_http_methods(["GET"])
def main(request):
    """Main page."""
    # Update database concerning available services.
    databaseIO.update_service_db()
    # Get names of all available services.
    available_service_name_list = filesystemIO.get_service_list()
    # Get names of all running services.
    running_service_name_list = rox_requests.get_running_services()
    # Send both lists to view.
    context = {"available_service_names": available_service_name_list,
               "running_service_names": running_service_name_list}
    return render(request, "web/web.html", context)


@require_http_methods(["POST"])
def start_service(request):
    """Start services specified in POST request's metadata."""
    # Get list of specified service names.
    service_name_list = request.POST.getlist("available_service_names")
    # Get list of corresponding JSON dictionaries.
    service_json_list = filesystemIO.get_service_jsons_from_filesystem(service_name_list)  # TODO: pull from DB
    # Start specified services and get list of JSON dictionaries
    # corresponding to all services which could not be started.
    error_json_list = rox_requests.start_services(service_json_list)
    if not error_json_list:
        # All services could be started.

        return redirect(views.main)
    else:
        # At least one service could not be started.

        # Convert JSON dictionaries to corresponding service name.
        error_name_list = []
        for error_json in error_json_list:
            error_name_list.append(error_json["params"]["name"])
        # Redirect to main page specifying all
        # service names which could not be started.
        error_name_string = ", ".join(error_name_list)
        messages.add_message(request, messages.WARNING, error_name_string)
        return redirect(views.main)


@require_http_methods(["POST"])
def stop_service(request):
    """Stop services specified in POST request's metadata."""
    # Get list of specified service names.
    service_name_list = request.POST.getlist("running_service_names")
    # Stop specified services and get list of names
    # corresponding to all services which could not be stopped.
    error_name_list = rox_requests.shutdown_services(service_name_list)
    if not error_name_list:
        # All services could be stopped.

        # Redirect to main page specifying all service
        # names which could not be stopped in metadata.
        return redirect(views.main)
    else:
        # At least one service could not be stopped.

        # Redirect to main page specifying all
        # service names which could not be stopped.
        error_name_string = ", ".join(error_name_list)
        messages.add_message(request, messages.WARNING, error_name_string)
        return redirect(views.main)
