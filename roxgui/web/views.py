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
import os

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

import databaseIO
import filesystemIO
import rox_request
from web import rox_logs
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
        rox_logs.save_log(request, msg_id=result.data)
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
