# encoding: utf-8
#
# Define URL patterns.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

from django.urls import path

from web import views
from web import rox_message
from web import rox_logs, rox_services

urlpatterns = [
    path('', views.main, name="web_main"),
    path("create_service", views.create_service, name="web_create_service"),
    path("start_service", views.start_service, name="web_start_service"),
    path("stop_service", views.stop_service, name="web_stop_service"),
    path("create_pipeline", views.create_pipeline, name="web_create_pipeline"),
    path("post_to_pipeline", views.post_to_pipeline, name="web_post_to_pipeline"),
    path("save_session", views.save_session, name="web_save_session"),
    path("load_session", views.load_session, name="web_load_session"),
    path("get_message_history", views.get_message_history, name="web_get_message_history"),
    path("delete_pipeline", views.delete_pipeline, name="web_delete_pipeline"),
    path("watch", views.watch, name="web_watch"),
    path("unwatch", views.unwatch, name="web_unwatch"),
    path("msg_status", rox_message.msg_status, name="web_msg_status"),
    path("get_log_json", rox_logs.get_log_json, name="web_get_log_json"),
    path("get_services", rox_services.get_services, name="web_get_services")
]
