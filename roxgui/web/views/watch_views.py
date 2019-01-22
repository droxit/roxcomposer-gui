# encoding: utf-8
#
# Define HTTP responses concering service watching with JSON data.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from web.local_request import file_request, rox_request
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

"""
@require_http_methods(["POST"])
def check_watched(request):
    result = rox_request.get_running_services()
    running_services = result.data
    services = request.POST.getlist("services[]", default=[])

    running = {}
    for service in services:
        service_is_running = False
        if service in running_services:
            service_is_running = True
        running[service] = service_is_running
    context = _create_json_context(running)
    return JsonResponse(context)
"""

@require_http_methods(["POST"])
def check_watched(request):
    check_session(request)
    print("Watched services:")
    print(request.session.get('watch_button_active', {}))
    context = _create_json_context(request.session.get('watch_button_active', {}))
    return JsonResponse(context)


def check_session(request):
    active = request.session.get('watch_button_active', {})
    if active == {}:
        logsess = rox_request.create_new_sess([]).data
        update_watch_buttons(request, logsess)
        request.session.modified = True


@require_http_methods(["POST"])
def watch(request):
    service_names = request.POST.getlist("services[]", default=[])
    cur_sess = request.session.get('current_session', None)
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
    """save the session to a json file """
    service_names = request.POST.getlist("services[]", default=[])
    cur_sess = request.session.get('current_session', None)
    res = rox_request.unwatch_services(service_names, cur_sess)
    if res.success:
        cur_sess = res.data
    else:
        print(res.message)
    update_watch_buttons(request, cur_sess)
    request.session.modified = True
    return JsonResponse(res.convert_to_json())

