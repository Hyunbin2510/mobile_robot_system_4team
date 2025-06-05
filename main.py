#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import UARTDevice
from mindsensorsPYB import LSA
import time

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
run_motor = Motor(Port.D)
steering_motor = Motor(Port.A)
ultra = UltrasonicSensor(Port.S4)
color_sensor = ColorSensor(Port.S2)
ser=UARTDevice(Port.S1,baudrate=115200)
lsa = LSA(Port.S3, 0X14)



# Write your program here.

########Function#########

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
    start_time = time.time

#Color sensor control function
def color_detection():
    r, g, b = color_sensor.rgb()
    #print(r,g,b)
    if 25 <= r <= 35 and 0 <= g <= 15 and 0 <= b <= 25:
        return "red"
    elif 35 <= r <= 45 and 45 <= g <= 55 and 25 <= b <= 35:
        return "yellow"
    return None

def isRedLight():
    try:
        p=ser.read_all().decode().strip()[-8:]
        return p=='redLight'
    
    except:
        pass

def red_detection_motion():
    # 레드 3번 감지 후 수행할 동작 구현
    ev3.speaker.beep()
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
        run_motor.run(250)
        yellow_stopped = True

########main########

start()
run_motor.run(250)

th = 30
Gain = 5
red_count=0
previous_color = None
yellow_stopped = False


while True:
    try:
        detected_color = color_detection()      
        if detected_color == "red" and previous_color != "red":
            ev3.speaker.beep()
            red_count += 1
            print(red_count)
            if red_count == 4:
                pass
            elif red_count == 5:
                run_motor.stop()
                steering_motor.stop()
                break
            
        elif detected_color == "yellow":
            yellow_detection_motion()

        # else:
        #     reset_yellow_flag()
        
        previous_color = detected_color

        # if not yellow_stopped:
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