# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    phone = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField()

    def __unicode__(self):
        return "%s,%s,%s" % (self.username, self.email, self.phone)

