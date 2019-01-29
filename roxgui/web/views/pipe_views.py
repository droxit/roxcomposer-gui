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
from web.views.json_views import _create_json_context



@require_http_methods(["POST"])
def get_pipelines(request):
    # Get JSON data of local pipelines.
    result = rox_request.get_pipelines()
    pipelines_json_dict = result.data
    # Prepare and return JSON response.
    context = _create_json_context(pipelines_json_dict)
    return JsonResponse(context)


@require_http_methods(["POST"])
def create_pipeline(request):
    # Get the service list that the pipe is supposed to contain
    services = request.POST.getlist("services[]", default=[])
    pipe_name = request.POST.get("pipe_name", default="")
    result = rox_request.create_pipeline(pipe_name, services)
    return JsonResponse({"data":result.data, "success":result.success, "message":result.message})


@require_http_methods(["POST"])
def get_pipeline_info(request):
    # Get the pipe name
    pipe_name = request.POST.get("pipe_name", default="")
    result = rox_request.get_pipelines() #get a list of all available pipelines
    print("PIPES: ", result.data)
    if pipe_name in result.data:
        print("PIPELINE:")
        print(result.data[pipe_name])

    #result = rox_request.create_pipeline(pipe_name, services)
    return JsonResponse({"data":result.data, "success":result.success, "message":result.message})
