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
from web.local_request import file_request, rox_request, rox_response


def _create_json_context(data) -> dict:
    """
    Create default context dictionary for JSON responses.
    :param data: Data structure which should be attached.
    :return: Default context dictionary for JSON responses.
    """
    context = {"data": data}
    return context


def create_rox_response(rox_result: rox_response.RoxResponse) ->JsonResponse:
    return JsonResponse({"data": rox_result.data, "success": rox_result.success, "message": rox_result.message})
