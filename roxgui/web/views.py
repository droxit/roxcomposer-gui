"""Configuration of web views."""

import rox_requests
from django.http import HttpResponseNotFound
from django.shortcuts import render


def web_main(request):
    """Main page."""
    if request.method == 'GET':
        response_dict = rox_requests.get_service_list()
        service_names = []
        service_jsons = []
        for s_name, s_json in response_dict.items():
            service_names.append(s_name)
            service_jsons.append(s_json)
        context = {"names": service_names, "jsons": service_jsons}
        return render(request, "web/web.html", context)
    elif request.method == "POST":
        return HttpResponseNotFound(request["services"])