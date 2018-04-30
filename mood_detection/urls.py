# -*- coding: utf-8 -*-
# @Author: Saurabh Agarwal
# @Date:   2018-03-09 18:37:55
# @Last Modified by:   saurabh
# @Last Modified time: 2018-04-30 22:49:35
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
	url(r'^$', views.home, name='home'),
]