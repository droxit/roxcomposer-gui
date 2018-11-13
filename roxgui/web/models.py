# encoding: utf-8
#
# Define database models.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

from django.db import models
import datetime

class Service(models.Model):
    name = models.CharField(max_length=200)
    service_json = models.TextField()

    def __str__(self):
        return self.name

class Logline(models.Model):
    service = models.CharField(max_length=200)
    msg = models.TextField()
    msg_id = models.CharField(max_length=200, default="")
    level = models.CharField(max_length=200, default='debug')
    time = models.DateTimeField()

    def __str__(self):
        logline = ""
        if self.msg_id:
            logline += "Message ID: {}, ".format(self.msg_id)
        if self.service:
            logline += "Service: {}, ".format(self.service)
        if self.msg :
            logline += "Message: {}, ".format(self.msg)
        if self.level:
            logline += "Loglevel: {}, ".format(self.level)
        if self.time:
            logline += "Time: {}".format(str(self.time))
        return logline

    def is_older(self, timeout_in_seconds):
        if self.time < datetime.datetime.now()-datetime.timedelta(seconds = timeout_in_seconds):
            return True
        return False

class Message(models.Model):
    msg_id = models.CharField(max_length=200, primary_key=True)
    pipeline = models.CharField(max_length=200, default="")

    def __str__(self):
        return "Message ID: {}, Pipeline: {}".format(self.msg_id, self.pipeline)


class RoxSession(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    services = models.TextField()
    timeout = models.IntegerField()

    def __str__(self):
        return "ID: {}, TIMEOUT: {}, SERVICES: {}.".format(str(self.id), str(self.timeout), str(self.services))
