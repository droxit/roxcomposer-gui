# encoding: utf-8
#
# Define HTTP responses with JSON data.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from web.local_request import file_request, rox_request


def _create_json_context(data) -> dict:
    """
    Create default context dictionary for JSON responses.
    :param data: Data structure which should be attached.
    :return: Default context dictionary for JSON responses.
    """
    context = {"data": data}
    return context


@require_http_methods(["POST"])
def get_services(request):
    # Get JSON data of local services.
    result = file_request.get_local_services()
    local_services_json_dict = result.data
    # Prepare and return JSON response.
    context = _create_json_context(local_services_json_dict)
    return JsonResponse(context)


@require_http_methods(["POST"])
def get_pipelines(request):
    # Get JSON data of local pipelines.
    result = rox_request.get_pipelines()
    pipelines_json_dict = result.data
    # Prepare and return JSON response.
    context = _create_json_context(pipelines_json_dict)
    return JsonResponse(context)
