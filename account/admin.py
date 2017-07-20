# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from account import models


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')

admin.site.register(models.User, UserAdmin)
