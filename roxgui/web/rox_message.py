from django.views.decorators.http import require_http_methods
import datetime
import json
import logging
import os
import time

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods

import databaseIO
import filesystemIO
import rox_request
from web import views
from web.models import Message, Logline, MessageStatus

@require_http_methods(["POST"])
def msg_status(request):
    pass
