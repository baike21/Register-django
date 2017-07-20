# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from account import views

# admin.autodiscover()


urlpatterns = {
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^changepasswd/$', views.changepasswd, name='changepasswd'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
}


