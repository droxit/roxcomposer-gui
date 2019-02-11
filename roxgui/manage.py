#!/usr/bin/python3
#
# encoding: utf-8
#
# Main entry point for Django backend.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#

import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roxgui.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
