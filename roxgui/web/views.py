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
from web.models import RoxSession, Logline
from rox_response import RoxResponse

removed_pipelines = []
LOG_RELOAD = 100
LOG_TIMEOUT = datetime.timedelta(days=10, hours=1, minutes=1, seconds=0, microseconds=0)
LOG_DELETE = datetime.timedelta(days=1)

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
            data = (key, value["services"], value["active"])
            pipeline_data_list.append(data)

    # retrieve the data for the selected pipeline
    selected_pipe = request.session.get('selected_pipe_name', "")
    selected_pipe_data = get_selected_pipe(selected_pipe, pipeline_data_list)

    # Get current logs.
    save_log(request)
    logs = get_logs()
    logging.info("Logs: "+ str(logs))
    logging.info("watch list: "+ str(request.session.get('watch_button_active', None)))

    # Send all data to view.
    context = {"available_services_dict": available_services_json_dict,
               "running_services_dict": running_services_json_dict,
               "pipeline_data": pipeline_data_list,
               "logs": logs,
               "selected_pipe": selected_pipe,
               "selected_pipe_services": selected_pipe_data['services'],
               "selected_pipe_active": selected_pipe_data['active'],
               "watch_active": request.session.get('watch_button_active',None)}
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
    port = request.POST.get("port")
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
    logging.info("START: " + str(service_name_list))
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
    """Create new pipeline."""
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
        response = {'status': 1, 'message': ("Ok")}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        messages.add_message(request, messages.ERROR, "Could not create pipeline.")
        response = {'status': 0, 'message': ("Your error")}
        return HttpResponse(json.dumps(response), content_type='application/json')


@require_http_methods(["POST"])
def select_pipeline(request):
    """
    Decide if new pipeline should be created or selected one should be edited. In either case save
    corresponding data to current session so that main view is able to render corresonding GUI elements.
    :param request: Request instance contains boolean flag "is_new_pipe" indicating if new pipeline should be created.
    If no new pipeline should be created, it also contains "pipe_name", "pipe_services" and "selected_pipe" parameters.
    :return: Redirect to main page with corresponding data in current session.
    """
    selected_pipeline = request.POST.get('pipe_name', default="")
    pipe_services = request.POST.get("pipe_services", default="")
    if pipe_services:
        pipe_services = eval(pipe_services)
    pipe_active = request.POST.get("selected_active", default="")
    request.session['selected_pipe_name'] = selected_pipeline
    request.session['selected_pipe_services'] = pipe_services
    request.session['selected_pipe_active'] = pipe_active
    return redirect(views.main)


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
    logging.error("POST TO PIPE: " + str(pipe_name))
    # Get message.
    pipe_message = request.POST.get("pipe_message_text", default="")
    logging.error("MSG: " + str(pipe_message))
    # Send message and get result.
    result = rox_request.post_to_pipeline(pipe_name, pipe_message)
    if result.success:
        # Message was sent successfully.
        logging.info("Message was sent successfully.")
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


@require_http_methods(["POST"])
def watch(request):
    """save the session to a json file """
    service_names = request.POST.get("services")
    #request.session['watch_button_active'] = {}
    request.session['watch_button_active'][service_names] = True
    request.session.modified = True
    service_names = [service_names]
    cur_sess = request.session.get('current_session', None)
    if cur_sess is not None:
        db_result = databaseIO.get_session(cur_sess)
        if db_result.success:
            # Current session's metadata could be achieved from database.
            rox_result = rox_request.watch_services(service_names, rox_session=db_result.data)
            rox_session = rox_result.data
            s = RoxSession(id=rox_session['id'], services=rox_session['services'], timeout=rox_session['timeout'])
            s.save()
        else:
            # Current session does not have any previously stored metadata, therefore create it.
            messages.warning(request, db_result.message)
            rox_result = rox_request.watch_services(service_names)
            request.session['current_session'] = rox_result.data
            request.session.modified = True
    else:
        rox_result = rox_request.watch_services(service_names)
        rox_session = rox_result.data
        session_services = ", ".join(list(rox_session['services']))
        s = RoxSession(id=rox_session['id'], services=session_services, timeout=rox_session['timeout'])
        s.save()
        request.session['current_session'] = rox_session['id']
        request.session.modified = True

    if rox_result.success:
        messages.success(request, rox_result.message)
        return redirect(views.main)
    else:
        messages.error(request, "Service could not be watched.")
        return redirect(views.main)


@require_http_methods(["POST"])
def unwatch(request):
    """save the session to a json file """
    service_names = request.POST.get("services")
    request.session['watch_button_active'][service_names] = False
    request.session.modified = True
    logging.info("UNWATCH: "+ str(service_names)+ str(request.session['watch_button_active']))
    cur_sess = request.session.get('current_session', None)
    if cur_sess is not None:
        logging.info("session: "+ str(cur_sess))
        dbResult = databaseIO.get_session(cur_sess)
        if dbResult.success:
            rox_session = dbResult.data
            result = rox_request.unwatch_services([service_names], rox_session)
            if result.success:
                s = RoxSession(id=rox_session['id'], services=rox_session['services'], timeout=rox_session['timeout'])
                s.save()
                messages.debug(request, result.message)
                return redirect(views.main)
            else:
                messages.error(request, "Couldn't unwatch services.")
                messages.debug(request, result.message)
                return redirect(views.main)
        else:
            messages.error(request, "Could not get session from database.")
            return redirect(views.main)
    else:
        messages.error(request, "No rox session active.")
        return redirect(views.main)



def get_response_values(request):
    mstring = []
    for key in request.POST.keys():  # "for key in request.GET" works too.
        # Add filtering logic here.
        valuelist = request.POST.getlist(key, default=[])
        mstring.extend(['%s=%s' % (key, val) for val in valuelist])
    return '&'.join(mstring)


def save_log(request, msg_id=None):
    """
    Get all new log messages from server.
    A log message can either be from watching services #TODO
    :param msg_id: optional, if the log concerns a specific message
    :return:
    """
    sess = request.session.get('current_session', None)
    logging.info("Trying to save logs, getting session: "+ str(sess))
    if sess is not None:  # if there is a current session write logs to database
        db_result = databaseIO.get_session(sess)  # retrieve current session
        logging.info("Accessing db with sess id: "+ str(db_result.success) + " msg: "+ str(db_result.message))
        if db_result.success:
            rox_result = rox_request.get_service_logs(rox_session = db_result.data)  # get the recent logs
            logging.info("Getting logs from server: "+ str(rox_result.success) + " \n" + str(rox_result.message))
            if rox_result.success:
                for log in rox_result.data:  # write each log line separately
                    if msg_id:  # TODO
                        l = Logline(msg_id=msg_id, service=log['service'], level=log['level'], msg=log['msg'],
                                    time=log['time'])
                    else:
                        l = Logline(service=log['service'], level=log['level'], msg=log['msg'], time=log['time'])
                    l.save()  # save to DB
            else: #could not retrieve logs with given session id, delete session
                create_new_sess(request)
        else:
            create_new_sess(request)
    else:
        create_new_sess(request)


def create_new_sess(request):
    services_to_be_watched = list(request.session.get('watch_button_active', {}).keys())
    res = rox_request.watch_services(services_to_be_watched)
    if res.success:
        request.session['current_session'] = res.data['id']
        request.session.modified = True
        logging.info("new sess created")
        update_session(res.data)
        messages.debug(request, "Services are being watched.")
    else:
        logging.info("haeh")
        messages.error(request, "Could not create new session.")

def update_session(rox_session):
    s = RoxSession(id=rox_session['id'], services=rox_session['services'], timeout=rox_session['timeout'])
    s.save()

def get_logs():
    # Create a datetime object spanning a full day
    dt_end = timezone.now()
    dt_start = dt_end - LOG_TIMEOUT
    dt_del_start = dt_end - LOG_DELETE

    Logline.objects.exclude(time__range=(dt_del_start, dt_end)).delete()

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
