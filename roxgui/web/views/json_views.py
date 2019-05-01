# encoding: utf-8
#
# Define HTTP responses with JSON data.
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

from django.http import JsonResponse
from web.local_request import rox_response


def _create_json_context(data) -> dict:
    """
    Create default context dictionary for JSON responses.
    :param data: Data structure which should be attached.
    :return: Default context dictionary for JSON responses.
    """
    context = {"data": data}
    return context


def create_rox_response(rox_result: rox_response.RoxResponse) -> JsonResponse:
    """
    Create a JsonResponse object for js-side operations containing
    a RoxResponse object (with the same message/data/success structure)
    :param rox_result: the RoxResponse object retrieved from communication with the ROXconnector
    :return: a JsonResponse object containing all information from the RoxResponse object
    """
    return JsonResponse({"data": rox_result.data, "success": rox_result.success, "message": rox_result.message})
