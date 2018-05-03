# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from keras.models import load_model
from .utils.datasets import get_labels
from .utils.inference import load_image
from .utils.inference import apply_offsets
from .utils.preprocessor import preprocess_input
from .utils.inference import detect_faces
from .utils.inference import load_detection_model
from .utils.inference import draw_text
from .utils.inference import draw_bounding_box
import keras
import sys
import cv2
import numpy as np
import os
import tempfile
# MYPATH = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0,MYPATH + '/face_classification/src/')
# sys.path.insert(0,MYPATH + '/face_classification/')
# from src import image_emotion_gender_demo
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
			# newdoc = Document(docfile = request.FILES['docfile'])
			f = tempfile.NamedTemporaryFile(delete=True)
			for chunk in request.FILES['docfile'].chunks():
				f.write(chunk)
			# f.write(ContentFile(request.FILES['docfile'].read()))
			# print(f.name)
			# newdoc.save()
			# print(type(request.FILES['docfile']))
			# print("#############",newdoc.docfile.path)
			# gender_model_path = './simple_CNN.81-0.96.hdf5'
			# imagePath = "/home/saurabh/Saurabh/viscom/viscom/media/documents/05/05/01/download_Aix0x5t.jpeg"
			# imagePath = newdoc.docfile.path
			imagePath = f.name
			detection_model_path =os.path.dirname(os.path.abspath(__file__)) + '/haarcascade_frontalface_default.xml'
			print("#################",detection_model_path)
			gender_model_path = os.path.dirname(os.path.abspath(__file__))+'/simple_CNN.81-0.96.hdf5'
			gender_classifier = load_model(gender_model_path, compile=False)
			
			emotion_model_path = os.path.dirname(os.path.abspath(__file__))+'/fer2013_mini_XCEPTION.102-0.66.hdf5'
			emotion_classifier = load_model(emotion_model_path, compile=False)



			face_detection = load_detection_model(detection_model_path)
			rgb_image = load_image(imagePath, grayscale=False)
			gray_image = load_image(imagePath, grayscale=True)
			gray_image = np.squeeze(gray_image)
			gray_image = gray_image.astype('uint8')
			faces = detect_faces(face_detection, gray_image)
			gender_offsets = (10, 10)
			emotion_offsets = (0, 0)
			gender_target_size = gender_classifier.input_shape[1:3]
			gender_labels = get_labels('imdb')
			emotion_labels = get_labels('fer2013')
			emotion_target_size = emotion_classifier.input_shape[1:3]
			for face_coordinates in faces:
			# 	print("Processing each face")
				x1, x2, y1, y2 = apply_offsets(face_coordinates, gender_offsets)
				rgb_face = rgb_image[y1:y2, x1:x2]

				x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
				gray_face = gray_image[y1:y2, x1:x2]

				try:
					rgb_face = cv2.resize(rgb_face, (gender_target_size))
					gray_face = cv2.resize(gray_face, (emotion_target_size))
				except:
					continue
				print(rgb_face.size)
				rgb_face = preprocess_input(rgb_face, False)
				rgb_face = np.expand_dims(rgb_face, 0)
			# 	print(rgb_face.size, gender_classifier.input_shape)
				gender_prediction = gender_classifier.predict(rgb_face)
				gender_label_arg = np.argmax(gender_prediction)
				gender_text = gender_labels[gender_label_arg]

				gray_face = preprocess_input(gray_face, True)
				gray_face = np.expand_dims(gray_face, 0)
				gray_face = np.expand_dims(gray_face, -1)
				emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
				emotion_text = emotion_labels[emotion_label_arg]

			# 	if gender_text == gender_labels[0]:
			# 		color = (0, 0, 255)
			# 	else:
			# 		color = (255, 0, 0)
			# 	print("Drawing around each image")
				if gender_text == gender_labels[0]:
					color = (0, 0, 255)
				else:
					color = (255, 0, 0)
				draw_bounding_box(face_coordinates, rgb_image, color)
				draw_text(face_coordinates, rgb_image, gender_text, color, 0, -20, 1, 2)
				draw_text(face_coordinates, rgb_image, emotion_text, color, 0, -50, 1, 2)
			# del gender_classifier
			# del gender_prediction
			bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
			print(os.path.dirname(os.path.abspath(__file__)) + '/predicted_test_image.png')
			cv2.imwrite(os.path.dirname(os.path.abspath(__file__)) + '/predicted_test_image.png', bgr_image)

			# image_emotion_gender_demo.readImage("/home/saurabh/Saurabh/viscom/viscom/media/documents/05/05/01/download_Aix0x5t.jpeg")
			# image_emotion_gender_demo.process()
			keras.backend.clear_session()
			return HttpResponseRedirect(reverse('mood_detection:list_file'))
		else:
			keras.backend.clear_session()
	else:
		keras.backend.clear_session()
		form = DocumentForm() # A empty, unbound form

	# Load documents for the list page
	documents = Document.objects.all()

	# Render list page with the documents and the form
	# return render(request,'mood_detection/home.html')
	return render(request,
		'mood_detection/home.html',
		{'documents': documents, 'form': form}
	)