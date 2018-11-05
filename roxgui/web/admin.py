# encoding: utf-8
#
# Define admin interface.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

from django.contrib import admin

from .models import Service

admin.site.register(Service)
