# encoding: utf-8
#
# Connect Django project to web server.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

"""
WSGI config for roxgui project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roxgui.settings')

application = get_wsgi_application()
