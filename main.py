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
    ULTRA_DISTANCE_THRESHHOLD = 100
    park_switch = [False, False, False,False, False]
    dist_lst = []

    while 1:
        temp = ultra.distance()
        
        
        print(park_switch)
        wait(100)


####################
    
########main########

start()
while 1:
    wait(100)
    buttons =  ev3.buttons.pressed()
    if Button.CENTER in buttons:
        break
start_time = time.time() # 시간 측정 시작작
run_motor.run(150)

th = 50
Gain = 3
red_count=0
previous_color = None
yellow_stopped = False


while True:
    try:
        detected_color = color_detection()
        
        if detected_color == "red" and previous_color != "red":
            red_count += 1
            if red_count == 4:
                red_detection_motion() 
            elif red_count == 5:
                run_motor.stop()
                steering_motor.stop()
            
        elif detected_color == "yellow":
            yellow_detection_motion()

        else:
            reset_yellow_flag()
        
        previous_color = detected_color

        if not yellow_stopped:
            data = lsa.ReadRaw_Calibrated()
            sensor_value = list(data)
            line_value = sensor_value[3]

            error = th - line_value
            correction = Gain * error
            correction = max(min(correction, 90), -90)

            steering_motor.run_target(1500, correction)

    except:
        pass
