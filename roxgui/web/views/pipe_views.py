# encoding: utf-8
#
# Define HTTP responses with JSON data concerning pipelines.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from web.local_request import rox_request
from web.views.json_views import create_rox_response
from web.models import Message
import datetime


@require_http_methods(["POST"])
def get_pipelines(request):
    """
    Get a json with all currently available pipelines from the ROXcomposer
    :param request: no data needed
    :return: JsonResponse containing the json of pipes
    """
    # Get JSON data of local pipelines.
    result = rox_request.get_pipelines()
    return JsonResponse(result.data)


@require_http_methods(["POST"])
def create_pipeline(request):
    """
    Create a new pipe on the ROXcomposer.
    Note that pipelines with the same name will be overwritten without prompt.
    :param request: shall contain a 'services' list and 'pipe_name' which is the name of the new pipe
    :return: The RoxResponse
    """
    # Get the service list that the pipe is supposed to contain
    services = request.POST.getlist("services[]", default=[])
    pipe_name = request.POST.get("pipe_name", default="")
    result = rox_request.create_pipeline(pipe_name, services)
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
                    time=datetime.datetime.now())
        m.save()
        #log_views.update_logs(request, msg_id=result.data)

    return create_rox_response(result)
