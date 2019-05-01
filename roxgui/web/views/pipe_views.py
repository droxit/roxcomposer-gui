# encoding: utf-8
#
# Define HTTP responses with JSON data concerning pipelines.
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

from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from web.local_request import rox_request
from web.models import Message
from web.views import log_views
from web.views.json_views import create_rox_response
import json
import uuid
from django.utils.encoding import smart_str
from roxgui import settings
import os


@require_http_methods(["POST"])
def get_pipelines(request):
    """
    Get a json with all currently available pipelines from the ROXcomposer
    :param request: no data needed
    :return: JsonResponse containing the json of pipes
    """
    # Get JSON data of local pipelines.
    result = rox_request.get_pipelines()
    return JsonResponse(result.convert_to_json())


@require_http_methods(["POST"])
def create_pipeline(request):
    """
    Create a new pipe on the ROXcomposer.
    Note that pipelines with the same name will be overwritten without prompt.
    :param request: shall contain a 'services' list and 'pipe_name' which is the name of the new pipe
    :return: The RoxResponse
    """
    # Get the service list that the pipe is supposed to contain
    services = json.loads(request.POST.get("services", default=""))
    pipe_name = request.POST.get("pipe_name", default="")
    result = rox_request.create_pipeline(pipe_name, services)
    return create_rox_response(result)


@require_http_methods(["POST"])
def delete_pipeline(request):
    """
    Delete a pipe on the ROXcomposer.
    :param request: shall contain a 'pipe_name' which is the name of the pipe that should be deleted
    :return: The RoxResponse
    """
    pipe_name = request.POST.get("pipe_name", default="")
    result = rox_request.remove_pipeline(pipe_name)
    return create_rox_response(result)


@require_http_methods(["POST"])
def get_pipeline_info(request):
    """
    Retrieve the pipeline information for a pipe name
    :param request: shall contain 'pipe_name', a string
    :return: a RoxResponse containing the pipe information
    """
    # Get the pipe name
    pipe_name = request.POST.get("pipe_name", default="")
    result = rox_request.get_pipelines()  # get a list of all available pipelines
    if pipe_name in result.data:
        result.data = result.data[pipe_name]
    else:
        result.data = {}
    return create_rox_response(result)


@require_http_methods(["POST"])
def send_msg(request):
    """
    Send a message to a pipe
    :param request: Shall contain 'pipe' a string with the pipeline name, 'msg' a string that is the message
    :return: A RoxResponse with the response message (and status) from the server
    """
    # Get the message and the pipe name
    pipe_name = request.POST.get("pipe", default="")
    msg = request.POST.get("msg", default="")
    # Send message and retrieve response
    result = rox_request.post_to_pipeline(pipe_name, msg)

    if result.success:
        # Message was sent successfully.
        m = Message(id=result.data, pipeline=pipe_name, message=msg,
                    time=timezone.now())
        m.save()
        log_views.update_logs(request, msg_id=result.data)

    return create_rox_response(result)


@require_http_methods(["GET"])
def save_session(request):
    """
    Download the session json file.
    :param request:
    :return: a json file containing the current session on the roxcomposer
    """
    file_name = "session-" + str(uuid.uuid4()) +".json"
    res = rox_request.save_session(file_name)
    file_path = res.data["filepath"]
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/blah')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
            response['X-Sendfile'] = smart_str(res.data["filepath"])
    else:
        response = create_rox_response(res)
    return response


@require_http_methods(["POST"])
def load_session(request):
    """
    Load a session on the roxcomposer from uploaded file.
    :param request:
    :return: response whether loading was successful
    """
    session = request.POST.get("session")
    print(session)
    res = rox_request.load_session(session)
    return create_rox_response(res)