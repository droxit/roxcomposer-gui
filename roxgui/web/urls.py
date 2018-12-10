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
from web import rox_logs, rox_services, rox_watch

urlpatterns = [
    path('', views.main, name="web_main"),
    path("create_service", views.create_service, name="web_create_service"),
    path("create_pipeline", views.create_pipeline, name="web_create_pipeline"),
    path("post_to_pipeline", views.post_to_pipeline, name="web_post_to_pipeline"),
    path("save_session", views.save_session, name="web_save_session"),
    path("load_session", views.load_session, name="web_load_session"),
    path("get_message_history", views.get_message_history, name="web_get_message_history"),
    path("delete_pipeline", views.delete_pipeline, name="web_delete_pipeline"),
    path("watch", rox_watch.watch, name="web_watch"),
    path("unwatch", rox_watch.unwatch, name="web_unwatch"),
    path("get_watched_status", rox_watch.get_watched_status, name="web_get_watched_status"),
    path("msg_status", rox_message.msg_status, name="web_msg_status"),
    path("get_log_json", rox_logs.get_log_json, name="web_get_log_json"),
    path("get_services", rox_services.get_services, name="web_get_services"),
    path("start_service", rox_services.start_service, name="web_start_service"),
    path("stop_service", rox_services.stop_service, name="web_stop_service"),

]
