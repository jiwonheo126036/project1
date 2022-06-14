from time import sleep
import threading
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from sensor import distance_scan
import cv2


pet_scan = 0
open_count = 0

GPIO.setmode(GPIO.BCM)
# Yellow : Pin 11 : 17(Trig)
GPIO.setup(17, GPIO.OUT)
# White : Pin 12 : 18(Echo)
GPIO.setup(18, GPIO.IN)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

def camera_start():

    global pet_scan

    face_classifier = cv2.CascadeClassifier('dog_face.xml')
    face_classifier2 = cv2.CascadeClassifier('haarcascade_frontalcatface_extended.xml')
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))
    else:
        print("No Camera")

    i=1
    while True:
        ret, frame = cap.read() 
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 얼굴 검출
            faces = face_classifier.detectMultiScale(gray,1.3,5)
            faces2 = face_classifier2.detectMultiScale(gray,1.3,5)
            
            for (x,y,w,h) in faces:
                if(w>120 and h>120):
                    cropped_face = frame[y:y+h, x:x+w].copy()
                    cropped_face = cv2.resize(cropped_face, dsize=(300, 300), 
                                                interpolation=cv2.INTER_AREA)
                    cv2.rectangle(frame, (x,y),(x+w, y+h), (0,0,255), 3)
                    pet_scan = 1
                    print(f"dog size {x} {y} {w} {h}")
                    

            for (x,y,w,h) in faces2:
                cropped_face = frame[y:y+h, x:x+w].copy()
                cropped_face = cv2.resize(cropped_face, dsize=(300, 300), 
                                            interpolation=cv2.INTER_AREA)
                cv2.rectangle(frame, (x,y),(x+w, y+h), (0,0,255), 3)
                pet_scan = 1
                print(f"cat size {x} {y} {w} {h}")


                #cv2.imshow('face', cropped_face)
            cv2.imshow('video', frame)

            if cv2.waitKey(1) == 27: break # ESC 키
        else:
            print('error')

    cap.release()
    cv2.destroyAllWindows()

def main():

    global pet_scan, open_count

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect('175.211.162.37', 1883)
    client.loop_start()

    t = threading.Thread(target=camera_start)
    t.start()

    while(1):
        if(pet_scan == 1):
            open_count = 6
            pet_scan = 0
        
        if(open_count > 0):
            open_count = open_count - 1
            print(open_count)
            if(distance_scan()<60):
                print("open")
                client.publish("Iot/door", "open")
                sleep(5)
                open_count = 0
                pet_scan = 0
        
        sleep(0.1)

    

try : 
    main()

except Exception as e:
    GPIO.cleanup()
    print(e)
    print("scan End")

