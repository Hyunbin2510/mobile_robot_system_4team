#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from mindsensorsPYB import LSA

import time

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
run_motor = Motor(Port.A)
steering_motor = Motor(Port.D)
ultra = UltrasonicSensor(Port.S4)
color_sensor = ColorSensor(Port.S3)
lsa = LSA(Port.S1, 0X14)



# Write your program here.
def start():
    '''
    steering_motor Calibration
    '''
    steering_motor.run(100)
    while 1:
        a = steering_motor.angle()
        wait(100)
        b = steering_motor.angle()

        if a == b:
            break

    steering_motor.stop()
    steering_motor.run_angle(-50, 100)
    steering_motor.reset_angle(0)
    
def steering_max(switch):
    '''
    왼쪽으로 쭉 조향을 꺾음
    switch = 1 : left
    switch = -1 : right
    '''
    steering_motor.run(switch * 100)
    while 1:
        a = steering_motor.angle()
        wait(100)
        b = steering_motor.angle()

        if a == b:
            break

    steering_motor.stop()

# calibration후 대기
start()
while 1:
    wait(100)
    buttons =  ev3.buttons.pressed()
    if Button.CENTER in buttons:
        break
start_time = time.time() # 시간 측정 시작작

# p_parking
run_motor.run(100)
ULTRA_DISTANCE_THRESHHOLD = 100
park_switch = [False, False, False,False, False]
dist_lst = []

while 1:
    temp = ultra.distance()
    
    
    print(park_switch)
    wait(100)

