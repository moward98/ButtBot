# NEED TO FIGURE OUT HOW BOT PHYSICALLY MOVES TO CHANGE PARAMETERS OF MOVEMENT FUNCTIONS
# WANT TO SPECIFY DISTANCE FOR FWD BWD, AND ANGLES FOR RIGHT AND LEFT
import math
import time
from constants import SLAVE_ADDR
import board
import busio
import time
import adafruit_pca9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

pca.frequency = 60

mtr1_dir = pca.channels[8]
mtr1_pwm = pca.channels[9] 
mtr2_dir = pca.channels[10]
mtr2_pwm = pca.channels[11]

class MotorDriver():

    def __init__(self, queue):
        self.q = queue
        self.HIGH = 0xFFFF
        self.LOW = 0x0000

    # Move both motors forwards at speed for duration
    def fwd_bwd(self, spd, dir):
            if dir == 'fwd':
                mtr1_dir.duty_cycle = self.HIGH
                mtr2_dir.duty_cycle = self.HIGH
            elif dir == 'bwd':
                mtr1_dir = self.HIGH
                mtr2_dir = self.LOW
            motor_speed = int(spd * 65535)
            mtr1_pwm.duty_cycle = motor_speed
            mtr2_pwm.duty_cycle = motor_speed

    # Move right motor backwards, while moving left motor forwards until desired angle
    def pivot(self, speed, dir):
            if dir == 'left':
                mtr1_dir.duty_cycle = self.LOW
                mtr2_dir = self.LOW
            elif dir == 'right':
                mtr1_dir = self.HIGH
                mtr2_dir = self.HIGH
            motor_speed = int(spd * 65535)
            mtr1_pwm.duty_cycle = motor_speed
            mtr2_pwm.duty_cycle = motor_speed

    # Stop both motors
    def stop(self):
            mtr1_pwm.duty_cycle = self.LOW
            mtr2_pwm.duty_cycle = self.LOW

    def motor_send(self, speed, duration, direction):
        print('sending cmd down motor q')
        data = [0,0,0]
        data[0] = speed
        data[1] = duration 
        data[2] = direction 
        self.q.put(data)

    def consumer(self):
        while True:
            data = self.q.get()
            if data[2] == 'fwd' or data[2] == 'bwd':
                print("sending command from motor q")
                self.fwd_bwd(data[0], data[2])
            elif data[2] == 'right' or data[2] == 'left':
                self.pivot(data[0],data[2])
            else:
                print("not a valid direction")
                self.stop()
                while True:
                    pass
            time.sleep(data[1])
            self.stop()

