# encoding: utf-8
#
# Define HTTP responses with HTML data.
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

from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def rox_home(request):
    """Main page."""
    context = {}
    return render(request, "web/pages/home/rox_home.html", context)


@require_http_methods(["GET"])
def rox_graph(request):
    """Graph page."""
    context = {}
    return render(request, "web/pages/graph/rox_graph.html", context)


@require_http_methods(["GET"])
def rox_messages(request):
    """Messages page."""
    context = {}
    return render(request, "web/pages/messages/rox_messages.html", context)


@require_http_methods(["GET"])
def rox_logs(request):
    """Logs page."""
    context = {}
    return render(request, "web/pages/logs/rox_logs.html", context)


@require_http_methods(["GET"])
def rox_pipelines(request):
    """Pipelines page."""
    context = {
        "search_bar_text": "Search pipelines",
        "headline": "Pipelines",
    }
    return render(request, "web/pages/pipelines/rox_pipelines.html", context)


@require_http_methods(["GET"])
def rox_services(request):
    """Services page."""
    context = {
        "search_bar_text": "Search services",
        "headline": "Services",

    }
    return render(request, "web/pages/services/rox_services.html", context)


@require_http_methods(["GET"])
def rox_tests(request):
    """Testing page."""
    context = {}
    return render(request, "web/pages/tests/rox_tests.html", context)
