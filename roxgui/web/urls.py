# encoding: utf-8
#
# Define URL patterns for web app.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

from django.urls import path

from web import views

urlpatterns = [
    path('', views.rox_main, name="rox_main"),
    path('graph', views.rox_graph, name="rox_graph"),
    path('messages', views.rox_messages, name="rox_messages"),
    path('logs', views.rox_logs, name="rox_logs"),
    path('pipelines', views.rox_pipelines, name="rox_pipelines"),
    path('services', views.rox_services, name="rox_services"),
]
