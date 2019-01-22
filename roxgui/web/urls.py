# encoding: utf-8
#
# Define URL patterns for web app.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

from django.urls import path
from web.views import html_views, json_views, watch_views, service_views

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
    path('get_pipelines', json_views.get_pipelines, name="get_pipelines"),

    #Service views
    path('get_services', service_views.get_services, name="get_services"),
    path('check_running', service_views.check_running, name="check_running"),
    path('start_services', service_views.start_services, name="start_services"),
    path('stop_services', service_views.stop_services, name="stop_services"),

    #Watch views
    path('check_watched', watch_views.check_watched, name="check_watched"),
    path('watch', watch_views.watch, name="watch"),
    path('unwatch', watch_views.unwatch, name="unwatch"),
]
