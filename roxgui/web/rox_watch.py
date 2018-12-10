import json
import logging

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

import rox_request

from web import views

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

    request.session.modified = True

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
