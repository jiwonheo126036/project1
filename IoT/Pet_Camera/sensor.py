import RPi.GPIO as GPIO
import time

def distance_scan():
    GPIO.output(17, False)
    time.sleep(0.5)

    GPIO.output(17, True)
    time.sleep(0.00001)
    GPIO.output(17, False)

    # 18번이 OFF가 되는 시점을 시작시간으로 설정
    while GPIO.input(18) == 0:
        start = time.time()

    # 18번이 ON이 되는 시점을 반사파 수신시간으로 설정
    while GPIO.input(18) == 1:
        stop = time.time()

    # 초음파가 되돌아오는 시간차로 거리를 계산한다
    time_interval = stop - start
    distance = time_interval * 17000
    distance = round(distance, 2)

    print("Distance => ", distance, "cm")
    
    return distance



if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)
    # Yellow : Pin 11 : 17(Trig)
    GPIO.setup(17, GPIO.OUT)
    # White : Pin 12 : 18(Echo)
    GPIO.setup(18, GPIO.IN)

    while 1:
        distance_scan()
