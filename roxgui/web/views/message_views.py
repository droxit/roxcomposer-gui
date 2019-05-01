# encoding: utf-8
#
# Define HTTP responses concerning messages sent to the ROXconnector and their status.
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU General Public License as published by |
# | the Free Software Foundation, either version 3 of the License, or    |
# | (at your option) any later version.                                  |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU General Public License           |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|
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
MSG_DELETE = datetime.timedelta(minutes=1)


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


def get_message_status(request, message):
    """
    For the current message retrieve the corresponding log lines from ROXcomposer trace log.
    These contain information on the current status of the message (e.g. the last service in the
    pipeline that was reached).
    Returns the MessageStatus Object that belongs to the Message Object.

    :param request: Contains the django session which is used to retrieve information on when the last
                    message poll (from the log file) happened
    :param message: a Message Object containing id and information regarding the message
    :return: a 'MessageStatus' object containing information on the current status of the message (or None if no
            message information is available)
    """
    res = rox_request.get_message_history(message.id)  # Retrieve trace log from ROXcomposer

    last_time = request.session.get('last_message_poll', None)  # Retrieve info on when logs were last pulled
    if res.success:  # Save the retrieved info as Loglines to DB
        tracelines = res.data
        for new_logline in tracelines:
            # new_logline = json.loads(line)
            msg_status = MessageStatus(event=new_logline['event'], status=new_logline['status'],
                                       time=epoch2dt(new_logline['time']), msg_id=new_logline['args']['message_id'],
                                       service_name=new_logline['args']['service_name'])
            if 'processing_time' in new_logline['args']:
                p_time = epoch2dt(new_logline['args']['processing_time'])
                if p_time.year == 1970:
                    msg_status.processing_time = p_time
                else:
                    msg_status.processing_time_long = p_time
            if 'total_processing_time' in new_logline['args']:
                p_time = epoch2dt(new_logline['args']['total_processing_time'])
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

    # retrieve only latest entry:
    if MessageStatus.objects.filter(msg_id=message.id).count() > 0:
        return MessageStatus.objects.filter(msg_id=message.id).latest('time')
    else:
        return None


@require_http_methods(["POST"])
def update_messages(request):
    """
    Retrieve the current messages and their status
    :param request: contains the django session variable
    :return: a JsonResponse containing all messages and their status as strings
    """
    msgs = get_messages()
    msg_dict = {}
    for msg in msgs:
        msg_status = get_message_status(request, msg)
        msg_dict[msg.id] = {"message": msg.to_dict(), "status": msg_status.to_dict()}

    return JsonResponse(msg_dict)


def epoch2dt(ts_epoch):
    """
    Converts an epoch timestamp to a human readable timestamp
    :param ts_epoch: epoch int
    :return: datetime timestamp
    """
    return timezone.make_aware(datetime.datetime.fromtimestamp(ts_epoch))
