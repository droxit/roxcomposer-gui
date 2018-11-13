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

import json
import databaseIO
import filesystemIO
import rox_requests
from web import views
from django.http import HttpResponse
from web.models import RoxSession, Logline

logger = logging.getLogger(__name__)


LOG_RELOAD = 100
LOG_TIMEOUT = 10000

@require_http_methods(["GET"])
def main(request):
    """Main page."""
    # Update database concerning available services.
    databaseIO.update_service_db()

    # Get names of all available services.
    available_service_name_list = filesystemIO.get_json_available_services()
    # Get names of all running services.
    res = rox_requests.get_name_running_services()
    running_service_name_list = res.data
    # Only consider non-running services as available.
    available_service_name_list = list(set(available_service_name_list) - set(running_service_name_list))

    # Get metadata of all available pipes.
    available_pipelines_json = rox_requests.get_pipelines()
    # Convert to list of tuples.
    pipeline_data_list = []

    #save_log()
    logs = get_logs()

    for key, value in available_pipelines_json.items():
        if key in rox_requests.removed_pipes:
            continue
        data = (key, value["services"], value["active"])
        pipeline_data_list.append(data)
    # Send all data to view.
    context = {"available_service_names": available_service_name_list,
               "running_service_names": running_service_name_list,
               "pipeline_data": pipeline_data_list,
               "logs":logs}
    return render(request, "web/web.html", context)


@require_http_methods(["POST"])
def start_service(request):
    """Start services specified in POST request's metadata."""
    # Get list of service names which should be started.
    service_name_list = request.POST.getlist("available_service_names", default=[])
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
        if not result.data:
            # No services were specified.
            messages.error(request, result.message)
            return redirect(views.main)
        else:
            # Some services were specified but could not be started.
            services_not_started = ", ".join(result.data)
            messages.error(request, "Unable to start service: {}.".format(services_not_started))
            return redirect(views.main)


@require_http_methods(["POST"])
def stop_service(request):
    """Stop services specified in POST request's metadata."""
    # Get list of service names which should be stopped.
    service_name_list = request.POST.getlist("running_service_names", default=[])
    # Stop specified services and get list of names
    # corresponding to all services which could not be stopped.
    res = rox_requests.shutdown_services(service_name_list)
    if res.success:
        # All services could be stopped.
        return redirect(views.main)
    else:
        # Some services could not be stopped.
        if not res.data:
            # No services were specified.
            messages.error(request, res.message)
            return redirect(views.main)
        else:
            # Some services were specified but could not be stopped.
            services_not_stopped = ", ".join(res.data)
            messages.error(request, "Unable to stop service: {}.".format(services_not_stopped))
            return redirect(views.main)


@require_http_methods(["POST"])
def create_pipeline(request):
    """Create new pipeline."""
    # Get list of service names which should be used for pipeline.
    service_name_list = request.POST.getlist("services[]", default=[])
    # Get pipe name.
    pipe_name = request.POST.get("name", "pipe_" + datetime.datetime.now().strftime("%Y%m%d%H%M"))
    # Create new pipeline.
    result = rox_requests.set_pipeline(pipe_name, service_name_list)
    if result:
        if pipe_name in rox_requests.removed_pipes:
            rox_requests.removed_pipes.remove(pipe_name)
        response = {'status': 1, 'message': ("Ok")}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        messages.add_message(request, messages.ERROR, "Could not create pipeline.")
        response = {'status': 0, 'message': ("Your error")}
        return HttpResponse(json.dumps(response), content_type='application/json')


@require_http_methods(["POST"])
def delete_pipeline(request):
    """Delete pipeline specified in POST request's metadata."""
    pipe_name = request.POST.get("pipe_name", "")
    rox_requests.removed_pipes.append(pipe_name)
    return redirect(views.main)



@require_http_methods(["POST"])
def post_to_pipeline(request):
    """Send message to pipeline specified in POST request's metadata."""
    # Get pipeline name.
    pipeline_name = request.POST.get("pipeline_name", default="")
    # Get message.
    message = request.POST.get("pipe_message", default="")
    # Send message and get result.
    result = rox_requests.post_to_pipeline(pipeline_name, message)
    if result.success:
        # Message was sent successfully.
        save_log(msg_id=result.data)
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
    result = rox_requests.save_session(file_name)
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
    result = rox_requests.load_session(file_name)
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
    message_id = request.POST.get("msg_id", "")
    result = rox_requests.get_msg_history(message_id)

    if result.success:
        messages.success(request, result.message)
        if result.message == "[]":
            messages.error(request, "Invalid message ID")
        else:
            messages.success(request, result.message)
        return redirect(views.main)
    else:
        messages.error(request, result.message)
        return redirect(views.main)


@require_http_methods(["POST"])
def watch(request):
    """save the session to a json file """

    service_names = request.POST.getlist("services[]")
    if rox_requests.current_session:
        rox_session = databaseIO.get_session(rox_requests.current_session)
        result = rox_requests.watch_services(service_names, rox_session=rox_session)
    else:
        result = rox_requests.watch_services(service_names)
        rox_session = result.data
        session_services = ", ".join(list(rox_session['services']))
        s = RoxSession(id=rox_session['id'], services=session_services, timeout=rox_session['timeout'])
        s.save()

        rox_requests.current_session = rox_session['id']


    if result.success:
        messages.debug(request, result.message)
        return redirect(views.main)
    else:
        messages.error(request, "Service could not be added to watchlist.")
        messages.debug(request, result.message)
        return redirect(views.main)

@require_http_methods(["POST"])
def get_service_logs(request):


    return redirect(views.main)


@require_http_methods(["POST"])
def unwatch(request):
    """save the session to a json file """
    service_names = request.POST.getlist("services[]")
    sess_id = rox_requests.current_session
    rox_session = databaseIO.get_session(sess_id)
    result = rox_requests.unwatch_services(service_names, rox_session = rox_session)


    if result.success:
        messages.debug(request, result.message)
        return redirect(views.main)
    else:
        messages.error(request, "Couldn't unwatch services.")
        messages.debug(request, result.message)
        return redirect(views.main)


def get_response_values(request):
    mstring = []
    for key in request.POST.keys():  # "for key in request.GET" works too.
        # Add filtering logic here.
        valuelist = request.POST.getlist(key, default=[])
        mstring.extend(['%s=%s' % (key, val) for val in valuelist])
    return '&'.join(mstring)

def save_log(msg_id = None):
    """
    Save all new log messages from server
    A log message can either be from watching services #TODO
    :param msg_id: optional, if the log concerns a specific message
    :return:
    """
    if rox_requests.current_session: #if there is a current session write logs to database
        sess = databaseIO.get_session(rox_requests.current_session) #retrieve current session
        response = rox_requests.get_service_logs(sess) #get the recent logs
        if response.data: #if there are any new log lines write them to database
            for log in response.data: #write each log line separately
                if msg_id: #TODO
                    l = Logline(msg_id=msg_id, service=log['service'], level=log['level'], msg=log['msg'], time=log['time'])
                else:
                    l = Logline(service=log['service'], level=log['level'], msg=log['msg'], time=log['time'])
                l.save() #save to DB

def get_logs():
    logs = Logline.objects.order_by('-time')[:LOG_RELOAD]
    return logs

def update_logs():
    pass
    #logs = Logline.objects.filter(time__range=(datetime.datetime.combine(d)))