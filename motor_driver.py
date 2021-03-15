# NEED TO FIGURE OUT HOW BOT PHYSICALLY MOVES TO CHANGE PARAMETERS OF MOVEMENT FUNCTIONS
# WANT TO SPECIFY DISTANCE FOR FWD BWD, AND ANGLES FOR RIGHT AND LEFT
import math
import time
from constants import SLAVE_ADDR
import time
import busio
#import board
import adafruit_pca9685
import Jetson.GPIO as GPIO
import smbus2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

i2c = smbus2.SMBus(1)
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 60

class MotorDriver():

    def __init__(self, queue):
        pca = adafruit_pca9685.PCA9685()
        pca.frequency = 60
        self.q = queue
        self.HIGH = 0xFFFF
        self.LOW = 0x0000
        self.mtr1_dir = pca.channels[8]
        self.mtr1_pwm = pca.channels[9] 
        self.mtr2_dir = pca.channels[10]
        self.mtr2_pwm = pca.channels[11]

    # Move both motors forwards at speed for duration
    def fwd_bwd(self, spd, dir):
            if dir == 'fwd':
                self.mtr1_dir.duty_cycle = self.HIGH
                self.mtr2_dir.duty_cycle = self.LOW
            elif dir == 'bwd':
                self.mtr1_dir.duty_cycle = self.LOW
                self.mtr2_dir.duty_cycle = self.HIGH
            motor_speed = int(spd * 65535)
            self.mtr1_pwm.duty_cycle = motor_speed - 2560
            self.mtr2_pwm.duty_cycle = motor_speed

    # Move right motor backwards, while moving left motor forwards until desired angle
    def pivot(self, spd, dir):
            if dir == 'left':
                self.mtr1_dir.duty_cycle = self.HIGH
                self.mtr2_dir.duty_cycle = self.HIGH
            elif dir == 'right':
                self.mtr1_dir.duty_cycle = self.LOW
                self.mtr2_dir.duty_cycle = self.LOW
            motor_speed = int(spd * 65535)
            self.mtr1_pwm.duty_cycle = motor_speed - 2560
            self.mtr2_pwm.duty_cycle = motor_speed

    # Stop both motors
    def stop(self):
            self.mtr1_pwm.duty_cycle = self.LOW
            self.mtr2_pwm.duty_cycle = self.LOW

    def motor_send(self, speed, duration, direction):
        data = [0,0,0]
        data[0] = speed
        data[1] = duration 
        data[2] = direction 
        self.q.put(data)

    def motor_consume(self):
        while True:
            data = self.q.get()
            print(data)
            if data[2] == 'fwd' or data[2] == 'bwd':
                self.fwd_bwd(data[0], data[2])
            elif data[2] == 'right' or data[2] == 'left':
                self.pivot(data[0],data[2])
            else:
                print("not a valid direction")
                self.stop()
            time.sleep(data[1])
            self.stop()

