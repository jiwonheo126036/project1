import cv2
import numpy as np

from haardetect import HaarDetect


img=cv2.imread('picture.jpg')#picture path


dog_face=HaarDetect('dog_face.xml')#used haarcascade Classifier
cat_face=HaarDetect('haarcascade_frontalcatface.xml path')#used haarcascade Classifier


cap = cv2.VideoCapture(0)
# cap.get(cv2.CAP_PROP_POS_FRAMES)
# cap.get(cv2.CAP_PROP_FRAME_COUNT)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)    (3)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)   (4)
if cap.isOpened():
    print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))
else:
  print("No Camera")

while True:
  ret, frame = cap.read()
  if ret:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 고양이 강아지 얼굴 검출
    facebox_dog = dog_face.detectMultiScale(gray,1.3,5)
    facebox_cat = cat_face.detectMultiscale(gray,1.3,5) 

    for (x,y,w,h) in facebox_dog:
        cropped_face1 = frame[y:y+h, x:x+w].copy()
        cropped_face1 = cv2.resize(cropped_face1, dsize=(300, 300),
                                interpolation=cv2.INTER_AREA)
        cv2.rectangle(frame, (x,y),(x+w, y+h), (0,0,255), 3)
    for (x,y,w,h) in facebox_cat:
        cropped_face2 = frame[y:y+h, x:x+w].copy()
        cropped_face2 = cv2.resize(cropped_face2, dsize=(300, 300),
                                interpolation=cv2.INTER_AREA)
        cv2.rectangle(frame, (x,y),(x+w, y+h), (0,0,255), 3)
    
    
    cv2.imshow('face', cropped_face1)
    cv2.imshow('face', cropped_face2)
    cv2.imshow('video', frame)
    if cv2.waitKey(1) == 27: break # ESC 키 
    else:
        print('error')
 
cap.release()
cv2.destroyAllWindows()