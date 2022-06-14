import RPi.GPIO as GPIO
import time
  
sensor = 17
  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(sensor,GPIO.IN)
print("Waiting for a sensor to settle.")
time.sleep(2)
  
while(True):
    if GPIO.input(sensor):
        print("Motion Detected")
        time.sleep(0.5)
    else:
        print("Motion not Detected")
        time.sleep(0.5)
    time.sleep(2)</code>