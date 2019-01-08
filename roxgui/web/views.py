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
def main(request):
    """Main page."""
    context = {}
    return render(request, "web/web.html", context)
