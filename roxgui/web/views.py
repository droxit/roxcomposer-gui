# encoding: utf-8
#
# Define web views.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def rox_main(request):
    """Main page."""
    context = {}
    return render(request, "web/rox_main.html", context)


@require_http_methods(["GET"])
def rox_graph(request):
    """Graph page."""
    context = {}
    return render(request, "web/rox_graph.html", context)


@require_http_methods(["GET"])
def rox_messages(request):
    """Messages page."""
    context = {}
    return render(request, "web/rox_messages.html", context)


@require_http_methods(["GET"])
def rox_logs(request):
    """Logs page."""
    context = {}
    return render(request, "web/rox_logs.html", context)


@require_http_methods(["GET"])
def rox_pipelines(request):
    """Pipelines page."""
    context = {}
    return render(request, "web/rox_pipelines.html", context)


@require_http_methods(["GET"])
def rox_services(request):
    """Services page."""
    context = {}
    return render(request, "web/rox_services.html", context)
