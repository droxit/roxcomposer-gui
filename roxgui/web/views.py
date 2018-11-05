# encoding: utf-8
#
# Define web views.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

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
    #Messaging Level
    messages.set_level(request, messages.DEBUG)
    #messages.set_level(request, messages.INFO)

    # Update database concerning available services.
    databaseIO.update_service_db()
    # Get names of all available services.
    available_service_name_list = filesystemIO.get_service_list()
    # Get names of all running services.
    running_service_name_list = rox_requests.get_running_services()
    #only show services that aren't already active in the available services menu
    available_service_name_list = list(set(available_service_name_list) - set(running_service_name_list))

    # Get metadata of all available pipes.
    available_pipelines_json = rox_requests.get_pipelines()
    # Convert to list of tuples.
    pipeline_data = []
    for key, value in available_pipelines_json.items():
        data = (key, value["services"], value["active"])
        pipeline_data.append(data)
    # Send all data to view.
    context = {"available_service_names": available_service_name_list,
               "running_service_names": running_service_name_list,
               "pipeline_data": pipeline_data}

    messages.set_level(request, messages.DEBUG)
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
    delivered, msg_list = rox_requests.start_services(service_json_list)
    if delivered:
        # All services could be started.

        return redirect(views.main)
    else:
        # At least one service could not be started.

        # Convert JSON dictionaries to corresponding service name.
        for error_service in msg_list:
            messages.add_message(request, messages.DEBUG, error_service)
            messages.add_message(request, messages.WARNING, "Could not start service.")

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

@require_http_methods(["POST"])
def post_to_pipeline(request):
    """Check if pipeline is active then send a message to specified pipeline"""
    # Get the pipeline name.
    pipeline_name = request.POST["pipeline_name"]
    # Get the message
    message = request.POST["pipe_message"]
    delivered, msg = rox_requests.post_to_pipeline(pipeline_name, message)
    if delivered:
        #message was sent
        messages.success(request, "Message posted.")
        messages.debug(request, msg)
        return redirect(views.main)
    else:
        #error while sending message
        messages.add_message(request, messages.DEBUG, msg)
        messages.add_message(request, messages.WARNING, "Message could not be sent.")
        return redirect(views.main)

@require_http_methods(["POST"])
def save_session(request):
    """save the session to a json file """
    dumpfile = request.POST["dumpfile"]
    dumped, msg = rox_requests.dump_everything(dumpfile)
    if dumped:
        messages.success(request, "Session saved as {}.".format(dumpfile))
        messages.debug(request, msg)
        return redirect(views.main)
    else:
        messages.error(request, "Session could not be saved.")
        messages.debug(request, msg)
        return redirect(views.main)

@require_http_methods(["POST"])
def load_session(request):
    """save the session to a json file """
    dumpfile = request.POST["dumpfile"]
    loaded, msg = rox_requests.restore_session(dumpfile)
    if loaded:
        messages.debug(request, msg)
        return redirect(views.main)
    else:
        messages.error(request, "Session could not be restored.")
        messages.debug(request, msg)
        return redirect(views.main)