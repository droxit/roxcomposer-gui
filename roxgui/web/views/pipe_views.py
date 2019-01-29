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
from web.local_request import file_request, rox_request
from web.views.json_views import create_rox_response



@require_http_methods(["POST"])
def get_pipelines(request):
    # Get JSON data of local pipelines.
    result = rox_request.get_pipelines()
    return JsonResponse(result.data)


@require_http_methods(["POST"])
def create_pipeline(request):
    # Get the service list that the pipe is supposed to contain
    services = request.POST.getlist("services[]", default=[])
    pipe_name = request.POST.get("pipe_name", default="")
    result = rox_request.create_pipeline(pipe_name, services)
    return create_rox_response(result)


@require_http_methods(["POST"])
def get_pipeline_info(request):
    # Get the pipe name
    pipe_name = request.POST.get("pipe_name", default="")
    result = rox_request.get_pipelines() #get a list of all available pipelines
    print("PIPES: ", result.data)
    if pipe_name in result.data:
        result.data = result.data[pipe_name]

    return create_rox_response(result)

@require_http_methods(["POST"])
def send_msg(request):
    # Get the message and the pipe name
    pipe_name = request.POST.get("pipe", default="")
    msg = request.POST.get("msg", default="")
    result = rox_request.post_to_pipeline(pipe_name, msg)
    return create_rox_response(result)
