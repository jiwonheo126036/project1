# # 이미지 캡쳐from time import sleep
# from picamera import PiCamera
# from datetime import datetime 

# import RPi.GPIO as GPIO
# # 이미지 캡쳐

# state = 0
# state_a = 0

# sensor = 17
  
# def capture():
#     nw = datetime.now()

#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     GPIO.setup(sensor,GPIO.IN)
#     print("Waiting for a sensor to settle.")

#     while True:
#         if GPIO.input(sensor) == True:
#             # Create File
#             camera = PiCamera()
#             camera.resolution = (320, 240)
#             camera.capture('{nw.year}-{nw.month}-{nw.day}_{nw.hour}:{nw.minute}:{nw.second}.jpg')
#             from .models import FaceImage
#             new_image = FaceImage('img{nw.year}-{nw.month}-{nw.day}_{nw.hour}:{nw.minute}:{nw.second}.jpg')
#             new_image.save()

#             camera.close()



# capture()
