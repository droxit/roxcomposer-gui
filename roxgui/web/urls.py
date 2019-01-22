# encoding: utf-8
#
# Define URL patterns for web app.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

from django.urls import path
from web.views import html_views, json_views

urlpatterns = [
    # HTML views.
    path('', html_views.rox_home, name="rox_home"),
    path('graph', html_views.rox_graph, name="rox_graph"),
    path('messages', html_views.rox_messages, name="rox_messages"),
    path('logs', html_views.rox_logs, name="rox_logs"),
    path('pipelines', html_views.rox_pipelines, name="rox_pipelines"),
    path('services', html_views.rox_services, name="rox_services"),
    path('tests', html_views.rox_tests, name="rox_tests"),

    # JSON views.
    path('get_services', json_views.get_services, name="get_services"),
    path('start_services', json_views.start_services, name="start_services"),
    path('stop_services', json_views.stop_services, name="stop_services"),
    path('get_pipelines', json_views.get_pipelines, name="get_pipelines"),
]
