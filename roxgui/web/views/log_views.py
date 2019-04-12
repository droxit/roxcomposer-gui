# encoding: utf-8
#
# Define HTTP responses concerning logs.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

import datetime
import logging
import json

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from web.local_request import rox_request
from web.models import Logline

# Only show this number of messages in log.
LOG_RELOAD = 100
# Only show logs received within this interval.
LOG_TIMEOUT = datetime.timedelta(minutes=1)
# Delete all logs from DB which are older than this interval.
LOG_DELETE = datetime.timedelta(days=1)
# The minimum loglevel of logs that should be shown
LOG_LEVEL = 40


@require_http_methods(["POST"])
def get_watch_logs(request):
    """ Retrieve the currently relevant logs from DB.
        New Loglines can be added from system logs, or
        when a service is watched and a Message is sent to a
        pipeline containing that service (the service must first receive the message, then
        the ROXcomposer sends a new log line). """
    # Get current logs.
    update_logs(request)
    logs = get_current_watch_logs()

    # Convert to dictionary of logs ({id: logline})
    log_dict_str = {}
    for log_line in logs:
        log_dict_str[log_line.id] = log_line.to_dict()
    return JsonResponse(log_dict_str)  # send as JsonResponse Object


def update_logs(request, msg_id=None):
    """
    Get new log messages from ROXcomposer and save them to database.
    :param request: Current request.
    :param msg_id: Specific message ID (default: None).
    """
    # update Service logs
    sess = request.session.get('current_session', {})
    if sess != {}:  # if there is a current session write new logs to database
        rox_result = rox_request.get_service_logs(sess)  # get the recent logs
        if rox_result.success:
            for log in rox_result.data:  # write each log line separately
                if msg_id:
                    new_logline = Logline(msg_id=msg_id, service=str(log['service']),
                                          level=log['level'], msg=str(log['msg']), time=log['time'])
                else:
                    new_logline = Logline(service=str(log['service']), level=log['level'], msg=str(log['msg']),
                                          time=log['time'])
                new_logline.save()  # save to DB
        else:
            logging.error("Error occurred while retrieving logs from ROXconnector: " + rox_result.message)
            start_new_session(request)
    else:  # no current session, can't get logs
        logging.error("Logs could not be retrieved as there is no session running.")

    # update system logs
    sys_sess = request.session.get('current_system_session', {})
    if sys_sess == {}:  # if no system logging session is currently running make a new one
        res = rox_request.create_new_roxcomposer_session()
        if res.success:  # if making new session was successful update logs with this session
            request.session["current_system_session"] = res.data
            request.session.modified = True
            update_system_logs(request, res.data)
        else:
            logging.error("System Logs could not be retrieved - {}".format(res.message))
    else:
        update_system_logs(request, sys_sess)  # update system logs with current session


def start_new_system_session(request):
    res = rox_request.create_new_roxcomposer_session()
    if res.success:  # if making new session was successful update logs with this session
        request.session["current_system_session"] = res.data
        request.session.modified = True


def update_system_logs(request, session):
    res = rox_request.get_system_logs(session)
    if res.success:
        for log in res.data:
            new_logline = Logline(level=log['level'], time=log['time'])
            try:
                full_log = json.dumps(log)
                new_logline.full_log = full_log
            except TypeError:
                if "msg" in log:
                    new_logline.msg = str(log["msg"])
                elif "message" in log:
                    new_logline.msg = str(log["message"])
            new_logline.save()
    else:
        logging.error("Error occurred while retrieving logs from ROXconnector: " + res.message)
        start_new_system_session(request)


def get_current_watch_logs():
    """
    Get recent log lines sorted by timestamp. Delete older logs if necessary.
    :return: QuerySet instance containing Logline objects.
    """
    dt_end = timezone.now()  # from now
    dt_start = dt_end - LOG_TIMEOUT  # till the time when the log messages time out
    dt_del_start = dt_end - LOG_DELETE  # logs older than this should be deleted from DB
    Logline.objects.exclude(time__range=(dt_del_start, dt_end)).delete()
    # load logs in a specific time range and then sort by time stamp, load only a certain amount of log lines
    logs = Logline.objects.filter(time__range=(dt_start, dt_end)).filter(level__gte=LOG_LEVEL).order_by('-time')[:LOG_RELOAD]
    return logs


def start_new_session(request):
    """ Begin a new session if the old one expired. """
    status = request.session.get('watch_button_active', None)
    request.session['current_session'] = {}
    if status is not None:
        services = list(status.keys())
        res = rox_request.create_new_sess(services)
        if res.success:
            new_session = res.data
            request.session['current_session'] = new_session
    request.session.modified = True
