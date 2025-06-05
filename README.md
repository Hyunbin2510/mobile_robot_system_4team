readme임다
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
    run_motor.run(150)
