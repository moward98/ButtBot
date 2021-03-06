from time import sleep
from adafruit_servokit import ServoKit
from constants import *
import Jetson.GPIO as GPIO
from pinout import FAN, ARM

## Servo[4] is for controlling collection arm. Mounted with 0 deg meaning arm is fully in down position
## Servo[5] controls the pitch of the camera. Mounted with 0 deg has camera pointing straight downwards
## Servo[9] and Servo[8] control the yaw of the camera. Servo[9] is mounted onto Servo[8].
## Mounted with 90 deg on both [9] and [8] at 90 deg means camera pointing straight forward


kit = ServoKit(channels=8)

def startup():
    ##Initial sweep Servo[8]
    #kit.servo[8].angle = 180
    sleep(0.45)
    #kit.servo[8].angle = 0
    #sleep(0.45)
    ##Initial sweep Servo[9]
    #kit.servo[9].angle = 180
    #sleep(0.45)
    #kit.servo[9].angle = 0
    #sleep(0.45)
    ##Initial sweep Servo[10]
    #kit.servo[5].angle = 180
    #sleep(0.45)
    #kit.servo[5].angle = 0
    #sleep(0.45)
    #Initial sweep arm
    #kit.servo[4].angle = 170
    #sleep(5)
    #kit.servo[4].angle = 0

#Return all servos to default position
def default():
    #kit.servo[8].angle = 90
    sleep(0.45)
    #kit.servo[9].angle = 90
    #sleep(0.45)
    #kit.servo[5].angle = 30
    #sleep(0.45)
    #kit.servo[4].angle = 7
    #sleep(0.45)

#Actuate arm for pickup routine
def arm():
    if GPIO.input(ARM):
        temp = GPIO.HIGH
    else:
        temp = GPIO.LOW
# turn on fan
    GPIO.output(FAN, GPIO.HIGH)
# lower arm
    GPIO.output(ARM, GPIO.LOW)
# wait 
    sleep(8)       
# raise arm
    GPIO.output(ARM, GPIO.HIGH)
# turn off fan
    GPIO.output(FAN, GPIO.LOW)
# wait
    sleep(1)
# return arm to prev state
    GPIO.output(ARM, temp)

def camera_tilt(pitch_angle):
    kit.servo[5].angle = pitch_angle

def camera_pan(butt_x, dir):
    if dir == 'right':    #to sweep right the servos will only be moving from 90 to 180 degrees
        min_angle = 90
        max_angle = 180
        inc = 1
    elif dir == 'left':   #to sweep left the servos will only be moving from 90 to 0 degrees
        min_angle = 0
        max_angle = 90
        inc = -1
    angle1 = sweep(min_angle, max_angle, inc, 9, butt_x) - 90        #Subtracts 90 to get the position w.r.t. the 90 degrees start point
    if angle1 == -90 or angle1 == 90:                        #If the first servo hasn't detected the marker in its max range
        angle2 = sweep(min_angle, max_angle, inc, 8, butt_x) - 90    #Move the second servo
    else:
        angle2 = 0
    angle_detected = angle1 + angle2                         #The marker is detected at the sum of both angles

def sweep(min_angle, max_angle, inc, servo_num, butt_x):
    angle = 90                                          #Servo always starting at default 90 deg
    for angle in range(min_angle, max_angle):           #Move servo degree by degree
        kit.servo[servo_num].angle = angle
        if(butt_x == IMG_WD/2):                             #If marker is detected return current servo angle
            return angle
        else:
            angle += inc                                  #Keep moving servo
        angle += inc

