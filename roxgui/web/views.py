# encoding: utf-8
#
# Define web views.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

import datetime
import logging

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

import databaseIO
import filesystemIO
import rox_requests
from web import views

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def main(request):
    """Main page."""
    # Update database concerning available services.
    databaseIO.update_service_db()

    # Get names of all available services.
    available_service_name_list = filesystemIO.get_service_list()
    # Get names of all running services.
    running_service_name_list = rox_requests.get_running_services()
    # Only consider non-running services as available.
    available_service_name_list = list(set(available_service_name_list) - set(running_service_name_list))

    # Get metadata of all available pipes.
    available_pipelines_json = rox_requests.get_pipelines()
    # Convert to list of tuples.
    pipeline_data_list = []
    for key, value in available_pipelines_json.items():
        data = (key, value["services"], value["active"])
        pipeline_data_list.append(data)
    # Send all data to view.
    context = {"available_service_names": available_service_name_list,
               "running_service_names": running_service_name_list,
               "pipeline_data": pipeline_data_list}
    return render(request, "web/web.html", context)


@require_http_methods(["POST"])
def start_service(request):
    """Start services specified in POST request's metadata."""
    # Get list of service names which should be started.
    service_name_list = request.POST.getlist("available_service_names")
    # Get list of corresponding JSON dictionaries.
    service_json_list = filesystemIO.get_service_jsons_from_filesystem(service_name_list)
    # Start specified services and get list of JSON dictionaries
    # corresponding to all services which could not be started.
    result = rox_requests.start_services(service_json_list)
    if result.success:
        # All services could be started.
        return redirect(views.main)
    else:
        # Some services could not be started.
        if not result_dict["data"]:
            # No services were specified.
            messages.error(request, result_dict["message"])
            return redirect(views.main)
        else:
            # Some services were specified but could not be started.
            services_not_started = ", ".join(result_dict["data"])
            messages.error(request, "Unable to start service: {}.".format(services_not_started))
            return redirect(views.main)


@require_http_methods(["POST"])
def stop_service(request):
    """Stop services specified in POST request's metadata."""
    # Get list of service names which should be stopped.
    service_name_list = request.POST.getlist("running_service_names")
    # Stop specified services and get list of names
    # corresponding to all services which could not be stopped.
    result = rox_requests.shutdown_services(service_name_list)
    if result.success:
        # All services could be stopped.
        return redirect(views.main)
    else:
        # Some services could not be stopped.
        if not result_dict["data"]:
            # No services were specified.
            messages.error(request, result_dict["message"])
            return redirect(views.main)
        else:
            # Some services were specified but could not be stopped.
            services_not_stopped = ", ".join(result_dict["data"])
            messages.error(request, "Unable to stop service: {}.".format(services_not_stopped))
            return redirect(views.main)


@require_http_methods(["POST"])
def create_pipeline(request):
    # Get list of service names which should be used for pipeline.
    service_name_list = request.POST.getlist("piped_service_names")
    # Create pipe name.
    pipe_name = "pipe_" + datetime.datetime.now().strftime("%Y%m%d%H%M")
    # Create new pipeline.
    result = rox_requests.set_pipeline(pipe_name, service_name_list)
    if result:
        return redirect(views.main)
    else:
        messages.add_message(request, messages.ERROR, "Could not create pipeline.")
        return redirect(views.main)


@require_http_methods(["POST"])
def post_to_pipeline(request):
    """Send message to specified pipeline."""
    # Get pipeline name.
    pipeline_name = request.POST["pipeline_name"]
    # Get message.
    message = request.POST["pipe_message"]
    # Send message and get result.
    result = rox_requests.post_to_pipeline(pipeline_name, message)
    if result.success:
        # Message was sent successfully.
        messages.success(request, result.msg)
        return redirect(views.main)
    else:
        # Error while sending message.
        messages.error(request, result.msg)
        return redirect(views.main)


@require_http_methods(["POST"])
def save_session(request):
    """save the session to a json file """
    dumpfile = request.POST["dumpfile"]
    result = rox_requests.dump_everything(dumpfile)
    if result.success:
        messages.success(request, "Session saved as {}.".format(dumpfile))
        messages.debug(request, result.msg)
        return redirect(views.main)
    else:
        messages.error(request, "Session could not be saved.")
        messages.debug(request, result.msg)
        return redirect(views.main)


@require_http_methods(["POST"])
def load_session(request):
    """save the session to a json file """
    dumpfile = request.POST["dumpfile"]
    result = rox_requests.restore_session(dumpfile)
    if result.success:
        messages.debug(request, result.msg)
        return redirect(views.main)
    else:
        messages.error(request, "Session could not be restored.")
        messages.debug(request, result.msg)
        return redirect(views.main)


@require_http_methods(["POST"])
def get_message_history(request):
    """Get history of a specified message."""
    message_id = request.POST["msg_id"]
    result = rox_requests.get_msg_history(message_id)
    if result.success:
        messages.success(request, result.msg)
        return redirect(views.main)
    else:
        messages.error(request, result.msg)
        return redirect(views.main)
