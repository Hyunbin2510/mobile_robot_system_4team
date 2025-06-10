#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from mindsensorsPYB import LSA
from pybricks.iodevices import UARTDevice
import time

'''
첫 기둥 확인하면 멈추기
'''

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
run_motor = Motor(Port.D)
steering_motor = Motor(Port.A)
ultra = UltrasonicSensor(Port.S4)
color_sensor = ColorSensor(Port.S2)
lsa = LSA(Port.S3, 0X14)
ser=UARTDevice(Port.S2,baudrate=115200)


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
    # print(r,g,b)

    if 25 <= r <= 35 and 0 <= g <= 15 and 0 <= b <= 30:
        return "red"
    elif 25 <= r <= 40 and 30 <= g <=45 and 15 <= b <= 35:
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
    global ULTRA_DISTANCE_THRESHOLD
    global count_num 
    global first_point_time
    global P_parking_flag
    temp = ultra.distance()
    print(temp)
    # print(temp)
    print(count_num)
    if count_num[0] < 2:
        if temp < ULTRA_DISTANCE_THRESHOLD:
            count_num[0] += 1
        
        if count_num[0] == 2:
            first_point_time = time.time()

    if count_num[1] < 1 and count_num[0] == 2:
        if temp > ULTRA_DISTANCE_THRESHOLD:
            count_num[1] += 1
    if count_num[2] < 1 and count_num[1] == 1:
        if temp < ULTRA_DISTANCE_THRESHOLD:
            count_num[2] += 1

    if count_num[2] == 1:
        second_point_time = time.time()
        diff_time = second_point_time - first_point_time
        print(diff_time)
        # print(first_point_time)
        # print(second_point_time)
        if diff_time < 2.5: # 짧은 구역 탐지 --> 주차장 지역으로 이동후 평행주차 실행
            print('짧 구역 탐지')
            run_motor.stop()
            steering_motor.run_target(80, -10)
            run_motor.run_target(150,run_motor.angle()+900)
            steering_motor.run_target(80, 100)
            run_motor.run_target(150,run_motor.angle()-450)
            steering_motor.run_target(80, -100)
            run_motor.run_target(150,run_motor.angle()-400)
            steering_motor.run_target(80, 0)
            run_motor.run_target(150,run_motor.angle()+100)
            steering_motor.run_target(80, -100)
            run_motor.run_target(150,run_motor.angle()-100)
            wait(500)
            # 나오기
            steering_motor.run_target(200, -100)
            run_motor.run_target(150,run_motor.angle()+400)

            steering_motor.run_target(200, 0)
            run_motor.run_target(150,run_motor.angle()+100)



            steering_motor.run_target(200, 100)
            run_motor.run_target(150,run_motor.angle()+600)

             
            P_parking_flag = True  
            run_motor.run(250)
            return

    if first_point_time > 2.5:
        
        diff_time1 = calcul_diff_time(first_point_time)
        print(diff_time1)
        if diff_time1 > 3: # 주차장 지역 --> 평행주차 실행
            print('주차장 탐지')
            run_motor.stop()
            steering_motor.run_target(80, -10)
            run_motor.run_target(150,run_motor.angle()+400)
            steering_motor.run_target(80, 100)
            run_motor.run_target(150,run_motor.angle()-450)
            steering_motor.run_target(80, -100)
            run_motor.run_target(150,run_motor.angle()-400)
            steering_motor.run_target(80, 0)
            run_motor.run_target(150,run_motor.angle()+100)
            steering_motor.run_target(80, -100)
            run_motor.run_target(150,run_motor.angle()-100)
            wait(500)
            # 나오기
            steering_motor.run_target(200, -100)
            run_motor.run_target(150,run_motor.angle()+400)

            steering_motor.run_target(200, 0)
            run_motor.run_target(150,run_motor.angle()+100)



            steering_motor.run_target(200, 100)
            run_motor.run_target(150,run_motor.angle()+600)

             
            P_parking_flag = True  
            run_motor.run(250)
            return

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
yellow_flag = False
ULTRA_DISTANCE_THRESHOLD = 150
count_num = [0,0,0,0,0]
first_point_time = 0
P_parking_flag = False


while True:
    try:
        if yellow_flag and not P_parking_flag: # 노란색 지난후 주차장 탐지
            p_parking()

        detected_color = color_detection()   
        # print(detected_color)
        # print(red_count)   
        if detected_color == "red" and previous_color != "red":
            ev3.speaker.beep()
            red_count += 1
            print(red_count)

            if red_count==3:
                run_motor.run(200)

            elif red_count == 4:
                run_motor.stop()

                while True:
                    p=ser.read_all().decode().strip()[-2:]
                    wait(500)
                    print(p)
                    if p=='00':
                        ev3.speaker.beep()
                        break
            
                run_motor.run(250)
                            
            elif red_count == 5:
                run_motor.stop()
                steering_motor.stop()
                break
            
        elif detected_color == "yellow" and not yellow_flag:
            yellow_detection_motion()
            yellow_flag = True
        
        previous_color = detected_color

        # if yellow_flag:
        #     Gain = 2

        data = lsa.ReadRaw_Calibrated()
        sensor_value = list(data)

        line_value1 = (sensor_value[6])
        line_value2 = (sensor_value[7])

        error1 = th - line_value1
        error2 = th - line_value2
        correction1 = Gain * error1
        correction2 = Gain * error2
        correction = max(min(max(correction1,correction2), 90), -90)

        steering_motor.run_target(1500, correction)

    except:
        pass




