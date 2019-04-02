# encoding: utf-8
#
# Define HTTP responses concerning service watching with JSON data.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from web.local_request import rox_request
from web.views.json_views import _create_json_context


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
def check_watched(request):
    """Check which services are being watched and which are not."""
    check_session(request)
    context = _create_json_context(request.session.get('watch_button_active', {}))
    return JsonResponse(context)


def check_session(request):
    """Check if a ROXcomposer session is active, if not create a new one"""
    current_session = request.session.get('current_session', {})
    # if there is no current session or no button status, reset both
    if 'id' not in current_session:
        reset_current_session(request)
        reset_watch_buttons(request)
    else:  # if there is a session, check if it is still valid and update watch buttons
        current_session = request.session.get('current_session', {})
        res = rox_request.get_logsession(current_session)
        if res.success:  # session is still valid
            current_session['services'] = list(res.data['services'])
            request.session["current_session"] = current_session
            request.session.modified = True
            update_watch_buttons(request, current_session) # update the watch buttons with new information
        else:  # session was not valid, reset current session and watch buttons
            reset_current_session(request)
            reset_watch_buttons(request)


def reset_current_session(request):
    """
    If something went wrong with the watching session reset the local copy
    :param request:
    :return:
    """
    request.session["current_session"] = {}
    request.session.modified = True
    return


def reset_watch_buttons(request):
    """
    If something went wrong with the watching session reset the watch button status of all services to 'unwatched'
    :param request:
    :return:
    """
    watch_buttons = request.session.get('watch_button_active', {})
    for service in watch_buttons:
        request.session['watch_button_active'][service] = False  # set everything to 'unwatched'
    request.session.modified = True
    return


@require_http_methods(["POST"])
def watch(request):
    """
    Watch specified services.
    :param request: Shall contain a 'services' list with the identifiers of all services that need to be watched
    :return: the response from the server
    """
    service_names = request.POST.getlist("services[]", default=[])
    cur_sess = request.session.get('current_session', {})

    res = rox_request.watch_services(service_names, rox_session=cur_sess)

    if res.success:  # the communication with ROXcomposer was successful: save the new session, update watch buttons
        new_sess = res.data
        request.session['current_session'] = new_sess
        update_watch_buttons(request, new_sess)  # update the buttons to watched/unwatched
        request.session.modified = True
    else:
        print(res.message)
    return JsonResponse(res.convert_to_json())


@require_http_methods(["POST"])
def unwatch(request):
    """unwatch specified services """
    service_names = request.POST.getlist("services[]", default=[])
    cur_sess = request.session.get('current_session', {})
    res = rox_request.unwatch_services(service_names, cur_sess)
    if res.success:
        cur_sess = res.data
    else:
        print(res.message)
    update_watch_buttons(request, cur_sess)
    request.session.modified = True
    return JsonResponse(res.convert_to_json())
