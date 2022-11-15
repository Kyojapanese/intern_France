#!/usr/bin/env python3
# File name   : move.py
# Description : Control Motor
# Product     : GWR
# Website     : www.gewbot.com
# Author      : William
# Date        : 2019/07/24
import time
import RPi.GPIO as GPIO
import servo
import threading
# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

Motor_A_EN    = 17
Motor_A_Pin1  = 27
Motor_A_Pin2  = 18

Dir_forward   = 1
Dir_backward  = 0

left_forward  = 1
left_backward = 0

right_forward = 1
right_backward= 0

forward=1
backward=0

pwn_A = 0
pwm_B = 0

def motorStop():#Motor stops
    GPIO.output(Motor_A_Pin1, GPIO.HIGH)
    GPIO.output(Motor_A_Pin2, GPIO.HIGH)
    GPIO.output(Motor_A_EN, GPIO.HIGH)
    
def setup():#Motor initialization
    global pwm_A, pwm_B
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    
    GPIO.setup(Motor_A_Pin1, GPIO.OUT)
    GPIO.setup(Motor_A_Pin2, GPIO.OUT)

    motorStop()
    try:
        pwm_A = GPIO.PWM(Motor_A_EN, 1000)
    except:
        pass

def motor(status, direction, speed):#Motor 1 positive and negative rotation
    if status == 0: # stop
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
    else:
        if direction == Dir_forward:#
            GPIO.output(Motor_A_Pin1, GPIO.HIGH)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            pwm_A.start(100)
            pwm_A.ChangeDutyCycle(speed)
        elif direction == Dir_backward:
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.HIGH)
            pwm_A.start(0)
            pwm_A.ChangeDutyCycle(speed)
    return direction


def move(speed, direction, turn, radius=0.6):   # 0 < radius <= 1
    #speed = 100
    if direction == 'forward':
        #if turn == 'right':
        motor(1, forward, speed)
        '''elif turn == 'left':
            motor(0, right_backward, int(speed*radius))
        else:
            motor(1, right_forward, speed)'''
    elif direction == 'backward':
        motor(1, backward, speed) 
        '''if turn == 'right':
            motor(1, right_backward, speed)
        elif turn == 'left':
            motor(0, right_forward, int(speed*radius))
        else:
            motor(1, right_backward, speed)'''
    elif direction == 'no':
        motor(1, backward, speed)
        '''if turn == 'right':
            motor(1, right_forward, speed)
        elif turn == 'left':
            motor(1, right_backward, speed)
        else:
            motorStop()'''
    else:
        pass




def destroy():
    motorStop()
    GPIO.cleanup()             # Release resource


if __name__ == '__main__':
    try:
#         servo.servo()
        speed_set = 60
        setup()
        move(speed_set, 'backward', 'no', 0.8)
        time.sleep(0.5)
        motorStop()
        destroy()
    except KeyboardInterrupt:
        destroy()
