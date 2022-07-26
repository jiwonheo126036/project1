# -*- coding: utf-8 -*-
"""FACES_test_6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LnIXj8Ij1E8GkIJqWG895JG_kvxVuQKV
"""

import numpy as np
import cv2
from urllib.request import Request, urlopen
from tensorflow.keras.models import load_model

model = load_model("/code/app/model/age_vggface_4.h5")
age_ranges = [0, 1, 2, 3, 4, 5, 6, 7]

gender_model = load_model("/code/app/model/gender_vgg16_fine_tuning_2.h5")
gender_ranges = [0, 1]

face_cascade = cv2.CascadeClassifier("/code/app/model/haarcascade_frontalface_default.xml")

#@title Define Necessary Functions { form-width: "5%", display-mode: "form" }

# Defining a function to shrink the detected face region by a scale for better prediction in the model.

def shrink_face_roi(x, y, w, h, scale=0.9):
    wh_multiplier = (1-scale)/2
    x_new = int(x + (w * wh_multiplier))
    y_new = int(y + (h * wh_multiplier))
    w_new = int(w * scale)
    h_new = int(h * scale)
    return (x_new, y_new, w_new, h_new)


# Defining a function to find faces in an image and then classify each found face into age-ranges defined above.

def classify_age(img):

    # Making a copy of the image for overlay of ages for passing to the loaded model for age classification.
    img_copy = np.copy(img)

    # Detecting faces in the image using the face_cascade loaded above and storing their coordinates into a list.
    faces = face_cascade.detectMultiScale(img_copy, scaleFactor=1.2, minNeighbors=6, minSize=(100, 100))
    
    if len(faces) > 0:
        # Looping through each face found in the image.
        for i, (x, y, w, h) in enumerate(faces):

            # Drawing a rectangle around the found face.
            face_rect = cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 100, 0), thickness=2)
            
            # Predicting the age of the found face using the model loaded above.
            x2, y2, w2, h2 = shrink_face_roi(x, y, w, h)
            face_roi = img[y2:y2+h2, x2:x2+w2]
            face_roi = cv2.resize(face_roi, (200, 200))
            face_roi = face_roi.reshape(-1, 200, 200, 3)
            face_age = age_ranges[np.argmax(model.predict(face_roi))]

        return face_age
    else:
        return 3

# Defining a function to find faces in an image and then classify each found face into gender-ranges defined above.

def classify_gender(img):

    # Making a copy of the image for overlay of ages for passing to the loaded model for gender classification.
    img_copy = np.copy(img)

    # Detecting faces in the image using the face_cascade loaded above and storing their coordinates into a list.
    faces = face_cascade.detectMultiScale(img_copy, scaleFactor=1.2, minNeighbors=6, minSize=(100, 100))
    
    if len(faces) > 0:
    # Looping through each face found in the image.
        for i, (x, y, w, h) in enumerate(faces):

            # Drawing a rectangle around the found face.
            face_rect = cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 100, 0), thickness=2)
            
            # Predicting the gender of the found face using the model loaded above.
            x2, y2, w2, h2 = shrink_face_roi(x, y, w, h)
            face_roi = img[y2:y2+h2, x2:x2+w2]
            face_roi = cv2.resize(face_roi, (200, 200))
            face_roi = face_roi.reshape(-1, 200, 200, 3)
            face_gender = gender_ranges[np.argmax(gender_model.predict(face_roi))]

        return face_gender
    else:
        return 1

#img = cv2.imread('img.jpg') 또는 iot 쪽에서 받아오는 값


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    image = np.asarray(bytearray(webpage.read()), dtype="uint8")
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return img