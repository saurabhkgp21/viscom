# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Create your views here.
def home(request):
	return render(request,'mood_detection/home.html')