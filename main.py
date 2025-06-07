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

'''
첫 기둥 확인하면 멈추기
'''

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

########Function#########

# Start function
def start():
    steering_motor.run(100)
    while True:
        a=steering_motor.angle()
        wait(100)
        b=steering_motor.angle()
        if a==b:
            break
        
    steering_motor.stop()
    steering_motor.run_angle(-100,100)
    steering_motor.reset_angle(0)
    
    while 1:
        wait(100)
        buttons =  ev3.buttons.pressed()
        if Button.CENTER in buttons:
            break
    start_time = time.time() # 시간 측정 시작작
    run_motor.run(250)
    
#Color sensor control function
def color_detection():
    r, g, b = color_sensor.rgb()

    if 50 <= r <= 100 and 0 <= g <= 40 and 0 <= b <= 40:
        return "red"
    elif 50 <= r <= 100 and 50 <= g <= 100 and 0 <= b <= 40:
        return "yellow"
    return None

def red_detection_motion():
    # 레드 3번 감지 후 수행할 동작 구현
    ev3.speaker.say("Red detected 3 times")
    # 여기에 추가 모션이나 신호등 감지 알고리즘 넣으면 됩니다

def yellow_detection_motion():
    global yellow_stopped
    if not yellow_stopped:
        run_motor.stop()
        steering_motor.stop()
        ev3.light.on(Color.RED)
        wait(1000)
        ev3.light.on(Color.YELLOW)
        wait(1000)
        ev3.light.on(Color.GREEN)
        wait(1000)
        run_motor.run(150)
        yellow_stopped = True

def reset_yellow_flag():
    global yellow_stopped
    yellow_stopped = False


# p_parking
def p_parking():
    ULTRA_DISTANCE_THRESHOLD = 100
    TIME_THRESHOLD = 1
    count_num = [0,0,0,0,0]
    dist_lst = []
    flag = False
    first_point_time = 0
    while 1:
        temp = ultra.distance()
        # print(temp)
        print(count_num)
        if count_num[0] < 3:
            if temp < ULTRA_DISTANCE_THRESHOLD:
                count_num[0] += 1
            
            if count_num[0] == 3:
                first_point_time = time.time()

        if count_num[1] < 3 and count_num[0] == 3:
            if temp > ULTRA_DISTANCE_THRESHOLD:
                count_num[1] += 1
        if count_num[2] < 3 and count_num[1] == 3:
            if temp <= ULTRA_DISTANCE_THRESHOLD:
                count_num[2] += 1

        if count_num[2] > 0:
            second_point_time = time.time()
            diff_time = second_point_time - first_point_time
            print(diff_time)
            # print(first_point_time)
            # print(second_point_time)
            if diff_time < 2.5: # 짧은 구역 탐지 --> 주차장 지역으로 이동후 평행주차 실행
                print('짧 구역 탐지')
                run_motor.stop()
                run_motor.run_target(150,run_motor.angle()+550)
                steering_motor.run_target(80, -100)
                run_motor.run_target(150,run_motor.angle()+400)
                steering_motor.run_target(80, 0)
                run_motor.run_target(150,run_motor.angle()-600)
                steering_motor.run_target(80, -100)
                run_motor.run_target(150,run_motor.angle()-300)
                steering_motor.run_target(80, 0)
                run_motor.run_target(150,run_motor.angle()+100)
                steering_motor.run_target(80, -100)
                run_motor.run_target(150,run_motor.angle()-100)
                wait(100)
                # 빠지는거
                run_motor.run_target(150,run_motor.angle()+300)
                steering_motor.run_target(80, 100)
                run_motor.run_target(150,run_motor.angle()+400)
                return

        if first_point_time > 2.5:
            
            diff_time1 = calcul_diff_time(first_point_time)
            print(diff_time1)
            if diff_time1 > 3: # 주차장 지역 --> 평행주차 실행
                print('주차장 탐지')
                run_motor.stop()
                # run_motor.run_target(150,run_motor.angle()+600)
                steering_motor.run_target(80, -100)
                run_motor.run_target(150,run_motor.angle()+400)
                steering_motor.run_target(80, 0)
                run_motor.run_target(150,run_motor.angle()-700)
                steering_motor.run_target(80, -100)
                run_motor.run_target(150,run_motor.angle()-300)
                steering_motor.run_target(80, 0)
                run_motor.run_target(150,run_motor.angle()+100)
                steering_motor.run_target(80, -100)
                run_motor.run_target(150,run_motor.angle()-100)
                return
        wait(100)

def calcul_diff_time(first_start_time):
    temp = time.time() - first_start_time
    return temp

####################
########main########

start()

th = 30
Gain = 5
red_count=0
previous_color = None
yellow_stopped = False



run_motor.run(150)  

p_parking()

run_motor.stop()




