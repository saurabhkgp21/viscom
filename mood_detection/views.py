# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Create your views here.
def home(request):
	print("here")
	return render(request,'mood_detection/home.html')

from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Document
from .forms import DocumentForm

def list(request):
	print(request.method)
	# Handle file upload
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save()
			print("sdf",newdoc.docfile.path, newdoc.docfile.url)

			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse('mood_detection:list_file'))
	else:
		form = DocumentForm() # A empty, unbound form

	# Load documents for the list page
	documents = Document.objects.all()

	# Render list page with the documents and the form
	# return render(request,'mood_detection/home.html')
	return render(request,
	    'mood_detection/home.html',
	    {'documents': documents, 'form': form}
	)