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
from django.utils import timezone
from django.views.decorators.http import require_http_methods

import databaseIO
import filesystemIO
import rox_request

from web import views
from web.models import Message, Logline

removed_pipelines = []

# Only show this number of messages in log.
LOG_RELOAD = 100
# Only show logs received within this interval.
LOG_TIMEOUT = datetime.timedelta(minutes=1)
# Delete all logs from DB which are older than this interval.
LOG_DELETE = datetime.timedelta(hours=1)


# Logging.
# ========
logging.basicConfig(filename="test.log", filemode='w', level=logging.DEBUG)


@require_http_methods(["GET"])
def main(request):
    """Main page."""
    # Update database concerning available services.
    databaseIO.update_service_db()

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

    # Get current logs.
    save_log(request)
    logs = get_logs()

    # Send all data to view.
    context = {"available_services_dict": available_services_json_dict,
               "running_services_dict": running_services_json_dict,
               "pipeline_data": pipeline_data_list,
               "logs": logs,
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
    # Check if given IP is valid.
    ip_parts = ip.split('.')
    for part in ip_parts:
        part = int(part)
        if not (0 <= part <= 255):
            return HttpResponse("Invalid IP address: {}.".format(ip))
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
    if res.success:
        messages.success(request, "Service created successfully.")
        return HttpResponse()
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
        save_log(request, msg_id=result.data)
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


def update_watch_buttons(request, logsession):
    """
    update the status of all watch buttons
    :param request: contains session object in which the status is saved
    :param logsession: the ROXconnector session that contains information about which services are being watched
    :return:
    """
    buttons_status = request.session.get('watch_button_active', None)  # get the current status of buttons

    if buttons_status is not None:
        buttons_services = list(buttons_status.keys())  # get all service names of current buttons
        for service in buttons_services:
            request.session['watch_button_active'][service] = False  # set everything to 'unwatched'
    else:
        request.session['watch_button_active'] = {}

    if logsession is not None:
        for service in logsession['services']:
            # for every watched service in session set to watched
            request.session['watch_button_active'][service] = True


@require_http_methods(["POST"])
def watch(request):
    service_name = request.POST.get("services")
    cur_sess = request.session.get('current_session', None)
    res = rox_request.watch_services([service_name], rox_session=cur_sess)
    if res.success:  # the communication with ROXcomposer was successful: save the new session, update watch buttons
        new_sess = res.data
        request.session['current_session'] = new_sess
        update_watch_buttons(request, new_sess)  # update the buttons to watched/unwatched
        request.session.modified = True

        messages.success(request, res.message)
        logging.info("Success watching: " + res.message)
        return redirect(views.main)
    else:
        logging.error("Error watching services: " + res.message)
        messages.error(request, "Error watching services: " + res.message)
        return redirect(views.main)


@require_http_methods(["POST"])
def unwatch(request):
    """save the session to a json file """
    service_names = request.POST.get("services")
    cur_sess = request.session.get('current_session', None)

    if cur_sess is not None:
        res = rox_request.unwatch_services([service_names], cur_sess)
        if res.success:
            cur_sess = res.data

            messages.debug(request, res.message)
        else:
            messages.error(request, "Couldn't unwatch services.")
            messages.debug(request, res.message)
    else:
        messages.error(request, "No rox session active.")

    update_watch_buttons(request, cur_sess)
    request.session.modified = True

    return redirect(views.main)


def get_response_values(request):
    mstring = []
    for key in request.POST.keys():  # "for key in request.GET" works too.
        # Add filtering logic here.
        valuelist = request.POST.getlist(key, default=[])
        mstring.extend(['%s=%s' % (key, val) for val in valuelist])
    return '&'.join(mstring)


def start_new_session(request):
    status = request.session.get('watch_button_active', None)
    if status is not None:
        services = list(status.keys())
        res = rox_request.create_new_sess(services)
        if res.success:
            new_session = res.data
            request.session['current_session'] = new_session
            request.session.modified = True


def save_log(request, msg_id=None):
    """
    Get all new log messages from server.
    A log message can either be from watching services #TODO
    :param msg_id: optional, if the log concerns a specific message
    :return:
    """

    sess = request.session.get('current_session', None)

    if sess is not None:  # if there is a current session write new logs to database
        rox_result = rox_request.get_service_logs(sess)  # get the recent logs
        if rox_result.success:
            for log in rox_result.data:  # write each log line separately
                logging.info("Log info: " + str(log))
                if msg_id:  # TODO
                    l = Logline(msg_id=msg_id, service=log['service'], level=log['level'], msg=log['msg'],
                                time=log['time'])
                else:
                    l = Logline(service=log['service'], level=log['level'], msg=log['msg'], time=log['time'])
                l.save()  # save to DB
        else:
            logging.error("Error occurred while retrieving logs from ROXconnector: " + rox_result.message)
            start_new_session(request)
    else:  # no current session, can't get logs
        logging.error("Logs could not be retrieved as there is no session running.")


def get_logs():
    """
    Load n log lines sorted by timestamp and delete old logs if necessary
    :return: a QuerySet object containing Logline objects
    """
    dt_end = timezone.now()  # from now
    dt_start = dt_end - LOG_TIMEOUT  # till the time when the log messages time out
    dt_del_start = dt_end - LOG_DELETE  # logs older than this should be deleted from DB

    Logline.objects.exclude(time__range=(dt_del_start, dt_end)).delete()
    # load logs in a specific time range and then sort by time stamp, load only a certain amount of log lines
    logs = Logline.objects.filter(time__range=(dt_start, dt_end)).order_by('-time')[:LOG_RELOAD]
    return logs


def update_logs():
    pass
    # logs = Logline.objects.filter(time__range=(datetime.datetime.combine(d)))


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
