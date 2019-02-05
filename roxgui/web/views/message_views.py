# encoding: utf-8
#
# Define HTTP responses concerning messages sent to the ROXconnector and their status.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#


import datetime
import json
import time

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from web.local_request import rox_request
from web.models import Message, MessageStatus

# Delete all messages which are older than this interval,
MSG_DELETE = datetime.timedelta(minutes=5)


def get_messages():
    """
    Retrieve the currently relevant messages from Database.
    :return: a Django QueryObject containing the current messages
    """
    # Get valid interval for messages.
    dt_end = timezone.now()
    dt_del_start = dt_end - MSG_DELETE
    # Delete all messages outside of this interval.
    Message.objects.exclude(time__range=(dt_del_start, dt_end)).delete()
    # Get all current messages ordered by time.
    msgs = Message.objects.all().order_by('-time')
    return msgs


def get_message_statuses(request, messages) -> dict:
    """
    For the current messages retrieve the corresponding log lines from ROXcomposer trace log.
    These contain information on the current status of the message (e.g. the last service in the
    pipeline that was reached).

    :param request: Contains the django session which is used to retrieve information on when the last
                    message poll (from the log file) happened
    :param messages: a Django QueryObject containing all currently relevant messages
    :return: a dictionary that for each message in 'messages' contains all status information as 'MessageStatus' objects
    """
    last_time = request.session.get('last_message_poll', None)
    res = rox_request.get_message_status(last_time=last_time)
    if res.success:
        tracelines = res.data
        for line in tracelines:
            l = json.loads(line)
            msg_status = MessageStatus(event=l['event'], status=l['status'], time=epoch2dt(l['time']),
                                       msg_id=l['args']['message_id'], service_name=l['args']['service_name'])
            if 'processing_time' in l['args']:
                p_time = epoch2dt(l['args']['processing_time'])
                if p_time.year == 1970:
                    msg_status.processing_time = p_time
                else:
                    msg_status.processing_time_long = p_time
            if 'total_processing_time' in l['args']:
                p_time = epoch2dt(l['args']['total_processing_time'])
                if p_time.year == 1970:
                    msg_status.total_processing_time = p_time
                else:
                    msg_status.total_processing_time_long = p_time

            msg_status.save()

    request.session['last_message_poll'] = time.time()
    request.session.modified = True

    dt_end = timezone.make_aware(datetime.datetime.now())
    dt_del_start = dt_end - MSG_DELETE
    MessageStatus.objects.exclude(time__range=(dt_del_start, dt_end)).delete()  # delete old entries

    # retrieve only latest entries of each message:
    msg_dict = {}

    for message in messages:
        if MessageStatus.objects.filter(msg_id=message.id).count() > 0:
            msg_dict[message] = MessageStatus.objects.filter(msg_id=message.id).latest('time')
        else:
            msg_dict[message] = None
    return msg_dict


@require_http_methods(["POST"])
def get_msg_status(request):
    """
    Retrieve the current messages and their status
    :param request: contains the django session variable
    :return: a JsonResponse containing all messages and their status as strings
    """
    msgs = get_messages()
    msg_dict = get_message_statuses(request, msgs)
    msg_dict_str = {}
    for msg in msg_dict:
        print("MESSAGE: ", msg_dict)
        msg_dict_str[msg.id] = {"message": msg.to_dict(), "status": msg_dict[msg].to_dict()}

    return JsonResponse(msg_dict_str)


def epoch2dt(ts_epoch):
    """
    Converts an epoch timestamp to a human readable timestamp
    :param ts_epoch: epoch int
    :return: datetime timestamp
    """
    return timezone.make_aware(datetime.datetime.fromtimestamp(ts_epoch))
