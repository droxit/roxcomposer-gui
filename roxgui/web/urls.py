# encoding: utf-8
#
# Define URL patterns for web app.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

from django.urls import path
from web.views import views, html_views, watch_views, service_views, pipe_views, message_views, log_views

urlpatterns = [
    # HTML views.
    path('', html_views.rox_home, name="web_rox_home"),
    path('graph', html_views.rox_graph, name="web_rox_graph"),
    path('messages', html_views.rox_messages, name="web_rox_messages"),
    path('logs', html_views.rox_logs, name="web_rox_logs"),
    path('pipelines', html_views.rox_pipelines, name="web_rox_pipelines"),
    path('services', html_views.rox_services, name="web_rox_services"),
    path('tests', html_views.rox_tests, name="web_rox_tests"),

    # Pipeline views.
    path('get_pipelines', pipe_views.get_pipelines, name="web_get_pipelines"),
    path('create_pipeline', pipe_views.create_pipeline, name="web_create_pipeline"),
    path('delete_pipeline', pipe_views.delete_pipeline, name="web_delete_pipeline"),
    path('get_pipeline_info', pipe_views.get_pipeline_info, name="web_get_pipeline_info"),
    path('send_msg', pipe_views.send_msg, name="web_send_msg"),
    path('pipelines/save_session', pipe_views.save_session, name="web_save_session"),
    path('load_session', pipe_views.load_session, name="web_load_session"),

    # Service views
    path('get_services', service_views.get_services, name="web_get_services"),
    path('get_running_services', service_views.get_running_services, name="web_get_running_services"),
    path('check_running', service_views.check_running, name="web_check_running"),
    path('start_services', service_views.start_services, name="web_start_services"),
    path('stop_services', service_views.stop_services, name="web_stop_services"),
    path('get_service_info', service_views.get_service_info, name="web_get_service_info"),
    path('get_service_info_specific_service', service_views.get_service_info_specific_service,
         name="web_get_service_info_specific_service"),
    path('delete_service', service_views.delete_service, name="web_delete_service"),
    path('create_service', service_views.create_service, name="web_create_service"),

    # Watch views
    path('check_watched', watch_views.check_watched, name="web_check_watched"),
    path('watch', watch_views.watch, name="watch"),
    path('unwatch', watch_views.unwatch, name="unwatch"),

    # Log Views
    path("get_watch_logs", log_views.get_watch_logs, name="web_get_watch_logs"),

    # Message Views
    path("update_messages", message_views.update_messages, name="web_update_messages"),

    # Manage config.ini file.
    path("check_rox_settings", views.check_rox_settings, name="web_check_rox_settings"),
    path("update_rox_settings", views.update_rox_settings, name="web_update_rox_settings"),
]
