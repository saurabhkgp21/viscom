# -*- coding: utf-8 -*-
# @Author: Saurabh Agarwal
# @Date:   2018-03-09 18:37:55
# @Last Modified by:   Saurabh Agarwal
# @Last Modified time: 2018-05-01 01:30:16
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = "mood_detection"

urlpatterns = [
	url(r'^$', views.list, name='list_file'),
]