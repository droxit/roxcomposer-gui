# encoding: utf-8
#
# Define HTTP responses with HTML data.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
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
        "headline": "Pipelines"
    }
    return render(request, "web/pages/pipelines/rox_pipelines.html", context)


@require_http_methods(["GET"])
def rox_services(request):
    """Services page."""
    context = {
        "search_bar_text": "Search services",
        "headline": "Services",
        "callback_func" : "create_service_detail",
        "callback_save": "save_service",
        "callback_run": "run_service",
    }
    return render(request, "web/pages/services/rox_services.html", context)


@require_http_methods(["GET"])
def rox_tests(request):
    """Testing page."""
    context = {}
    return render(request, "web/pages/tests/rox_tests.html", context)
