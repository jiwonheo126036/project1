import boto3
from botocore.client import Config

ACCESS_KEY_ID = 'AKIA5VZTIAOJXRWANKEK' #s3 관련 권한을 가진 IAM계정 정보
ACCESS_SECRET_KEY = 'Tx1LUyM2dcY9AB0SGCd8wYKDYYFPY7e6yaiRCXwR'
BUCKET_NAME = 'langhae-20220525'


# def image_upload():
#     data = open('/home/pi/workspace/finalproject/IMG_1852.JPG','rb')
#     s3 = boto3.resource(
#         's3',
#         aws_access_key_id=ACCESS_KEY_ID,
#         aws_secret_access_key=ACCESS_SECRET_KEY,
#         config=Config(signature_version='s3v4')
#     )
#     s3.Bucket(BUCKET_NAME).put_object(
#         Key='IMG_1852.JPG', Body=data, ContentType='image/jpg')

# image_upload()

from time import sleep
from picamera import PiCamera
from datetime import datetime 

import RPi.GPIO as GPIO

# 이미지 캡쳐

state = 0
state_a = 0

sensor = 17
  
def capture():
    nw = datetime.now()

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(sensor,GPIO.IN)
    print("Waiting for a sensor to settle.")

    while True:
        if GPIO.input(sensor) == True:
            print("Motion detected")
            # Create File
            
            camera = PiCamera()
            camera.resolution = (320, 240)
            camera.start_preview()
            sleep(2)
            camera.capture(f'img{nw.year}-{nw.month}-{nw.day}_{nw.hour}:{nw.minute}:{nw.second}.jpg')
            print("camera capture")
            # camera.stop_preview()

            # Read File
            f = open(f"img{nw.year}-{nw.month}-{nw.day}_{nw.hour}:{nw.minute}:{nw.second}.jpg","rb")
            s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
            )
            s3.Bucket(BUCKET_NAME).put_object(
            Key = f"img{nw.year}-{nw.month}-{nw.day}_{nw.hour}:{nw.minute}:{nw.second}.jpg", Body = f, ContentType='image/jpg')
            print("image send")
capture()