# encoding: utf-8
#
# Define web views.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

import datetime
import json
import logging

from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

import databaseIO
import filesystemIO
import rox_request
from web import log_views
from web import views
from web.models import Message

removed_pipelines = []

# Logging.
# ========
logging.basicConfig(filename="test.log", filemode='w', level=logging.DEBUG)


@require_http_methods(["GET"])
def main(request):
    """Main page."""
    # Update database concerning available services.
    databaseIO.update_service_db()

    # for key in list(request.session.keys()):
    #    del request.session[key]

    # Get JSON data of all available services (excluding forbidden ones).
    file_result = filesystemIO.get_available_service_jsons()
    available_services_json_dict = file_result.data
    # Get JSON data of all running services (excluding forbidden ones).
    rox_result = rox_request.get_running_service_jsons()
    running_services_json_dict = rox_result.data
    # Only consider services which are currently not running as available.
    tmp_dict = {}
    for key, value in available_services_json_dict.items():
        if key not in running_services_json_dict:
            tmp_dict[key] = value
    available_services_json_dict = tmp_dict

    # Get metadata of all available pipes.
    res = rox_request.get_pipelines()
    available_pipeline_json_dict = res.data
    # Convert to list of tuples.
    pipeline_data_list = []
    if res.success:
        for key, value in available_pipeline_json_dict.items():
            if key in rox_request.removed_pipes:
                continue
            data = (key, json.dumps(value["services"]), value["active"])
            pipeline_data_list.append(data)

    # Send all data to view.
    context = {"available_services_dict": available_services_json_dict,
               "running_services_dict": running_services_json_dict,
               "pipeline_data": pipeline_data_list,
               "watch_active": request.session.get('watch_button_active', None)
               }
    return render(request, "web/web.html", context)


@require_http_methods(["POST"])
def create_service(request):
    """Create service specified in POST request's metadata."""
    # Mandatory parameters.
    # =====================

    # Get IP address.
    ip = request.POST.get("ip")
    # Get port number.
    port = int(request.POST.get("port"))
    # Get service name.
    name = request.POST.get("name")
    # Get classpath.
    class_path = request.POST.get("class_path")

    # Optional parameters.
    # ====================

    optional_param_keys = request.POST.getlist("optional_param_keys[]", default=[])
    optional_param_values = request.POST.getlist("optional_param_values[]", default=[])

    res = rox_request.create_service(ip, port, name, class_path, optional_param_keys, optional_param_values)
    res_json = res.convert_to_json()
    return JsonResponse(res_json)


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


@require_http_methods(["POST"])
def create_pipeline(request):
    """Create or update pipeline."""
    # Get list of service names which should be used for pipeline.
    service_name_list = request.POST.getlist("services[]", default=[])
    # Get pipe name.
    pipe_name = request.POST.get("name")
    if not pipe_name:
        pipe_name = "pipe_" + datetime.datetime.now().strftime("%Y%m%d%H%M")
    # Create new pipeline.
    res = rox_request.create_pipeline(pipe_name, service_name_list)
    if res.success:
        if pipe_name in rox_request.removed_pipes:
            rox_request.removed_pipes.remove(pipe_name)
        response = {'status': 1, 'message': "Ok"}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        messages.add_message(request, messages.ERROR, "Could not create pipeline.")
        response = {'status': 0, 'message': "Your error"}
        return HttpResponse(json.dumps(response), content_type='application/json')


@require_http_methods(["POST"])
def delete_pipeline(request):
    """Delete pipeline specified in POST request's metadata."""
    pipe_name = request.POST.get("pipe_name", "")
    rox_request.removed_pipes.append(pipe_name)
    return redirect(views.main)


@require_http_methods(["POST"])
def post_to_pipeline(request):
    """Send message to pipeline specified in POST request's metadata."""
    # Get pipeline name.
    pipe_name = request.POST.get("pipe_name", default="")
    # Get message.
    pipe_message = request.POST.get("pipe_message_text", default="")
    # Send message and get result.
    result = rox_request.post_to_pipeline(pipe_name, pipe_message)
    if result.success:
        # Message was sent successfully.
        m = Message(id=result.data, pipeline=pipe_name, message=pipe_message,
                    time=datetime.datetime.now())
        m.save()
        log_views.update_logs(request, msg_id=result.data)
        messages.success(request, result.message)
        return redirect(views.main)
    else:
        # Error while sending message.
        messages.error(request, result.message)
        return redirect(views.main)


@require_http_methods(["POST"])
def save_session(request):
    """Save current session to JSON file."""
    file_name = request.POST.get("save_file_name", default="")
    result = rox_request.save_session(file_name)
    if result.success:
        messages.success(request, "Session saved as {}.".format(file_name))
        messages.debug(request, result.message)
        return redirect(views.main)
    else:
        messages.error(request, "Session could not be saved.")
        messages.debug(request, result.message)
        return redirect(views.main)


@require_http_methods(["POST"])
def load_session(request):
    """Load session from JSON file."""
    file_name = request.POST.get("load_file_name", default="")
    result = rox_request.load_session(file_name)
    if result.success:
        messages.debug(request, result.message)
        return redirect(views.main)
    else:
        messages.error(request, "Session could not be restored.")
        messages.debug(request, result.message)
        return redirect(views.main)


@require_http_methods(["POST"])
def get_message_history(request):
    """Get history of a specified message."""
    pipe_message_id = request.POST.get("pipe_message_id", "")
    result = rox_request.get_message_history(pipe_message_id)
    if result.success:
        messages.success(request, result.data)
        return redirect(views.main)
    else:
        messages.error(request, result.message)
        return redirect(views.main)


def get_response_values(request):
    mstring = []
    for key in request.POST.keys():  # "for key in request.GET" works too.
        # Add filtering logic here.
        valuelist = request.POST.getlist(key, default=[])
        mstring.extend(['%s=%s' % (key, val) for val in valuelist])
    return '&'.join(mstring)


def get_selected_pipe(pipe_name, pipe_list):
    """ convert the pipe list of tuples to a dictionary and get the data for pipe_name"""
    if pipe_name == "":
        return {'active': False, 'services': []}
    pipe_dict = {data[0]: {'active': data[2], 'services': data[1]} for data in pipe_list}

    if pipe_name in pipe_dict:
        selected = pipe_dict[pipe_name]
        return selected
    else:
        return {'active': False, 'services': []}
