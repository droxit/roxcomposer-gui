# encoding: utf-8
#
# Define database models.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=200)
    service_json = models.TextField()

    def __str__(self):
        return self.name

class Logline(models.Model):
    service = models.CharField(max_length=200)
    msg = models.TextField()

class RoxSession(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    services = models.TextField()
    timeout = models.IntegerField()

    def __str__(self):
        return self.id
