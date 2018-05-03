# -*- coding: utf-8 -*-
# @Author: Saurabh Agarwal
# @Date:   2018-05-01 14:59:44
# @Last Modified by:   Saurabh Agarwal
# @Last Modified time: 2018-05-01 17:06:16
import sys
sys.path.insert(0,"./face_classification/src/")
from face_classification.src import image_emotion_gender_demo

image_emotion_gender_demo.readImage("/home/saurabh/Saurabh/viscom/viscom/media/documents/05/05/01/download_Aix0x5t.jpeg")
image_emotion_gender_demo.process()