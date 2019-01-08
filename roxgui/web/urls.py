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
    path('', views.main, name="web_main"),
]
