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
