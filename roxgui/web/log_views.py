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

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

import rox_request
from web.models import Logline

# Only show this number of messages in log.
LOG_RELOAD = 100
# Only show logs received within this interval.
LOG_TIMEOUT = datetime.timedelta(minutes=1)
# Delete all logs from DB which are older than this interval.
LOG_DELETE = datetime.timedelta(hours=1)

# Logging.
# ========
logging.basicConfig(filename="test.log", filemode='w', level=logging.DEBUG)


@require_http_methods(["POST"])
def get_watch_logs(request):
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
    sess = request.session.get('current_session', None)
    if sess is not None:  # if there is a current session write new logs to database
        rox_result = rox_request.get_service_logs(sess)  # get the recent logs
        if rox_result.success:
            for log in rox_result.data:  # write each log line separately
                if msg_id:
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
    logs = Logline.objects.filter(time__range=(dt_start, dt_end)).order_by('-time')[:LOG_RELOAD]
    return logs


def start_new_session(request):
    status = request.session.get('watch_button_active', None)
    if status is not None:
        services = list(status.keys())
        res = rox_request.create_new_sess(services)
        if res.success:
            new_session = res.data
            request.session['current_session'] = new_session
            request.session.modified = True
