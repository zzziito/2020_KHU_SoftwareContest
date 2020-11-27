import time
import busio

from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor


class drivingclass:

    def __init__(self):
        print("init.............")
        self.i2c = busio.I2C(SCL, SDA)

        self.pca = PCA9685(self.i2c, address=0x40)
        self.pca.frequency = 100

        self.pca.channels[4].duty_cycle = 0xFFFF
        self.pca.channels[9].duty_cycle = 0xFFFF
        self.pca.channels[15].duty_cycle = 0xFFFF
        self.pca.channels[10].duty_cycle = 0xFFFF

        self.motor1 = motor.DCMotor(self.pca.channels[5], self.pca.channels[6])
        self.motor2 = motor.DCMotor(self.pca.channels[8], self.pca.channels[7])
        self.motor3 = motor.DCMotor(
            self.pca.channels[14], self.pca.channels[13])
        self.motor4 = motor.DCMotor(
            self.pca.channels[11], self.pca.channels[12])
        print("init.............finish")

    def goForward(self, speed):
        print(self)
        self.motor1.throttle = speed
        self.motor2.throttle = speed
        self.motor3.throttle = speed
        self.motor4.throttle = speed
        time.sleep(1)

    def goBackward(self, speed):
        self.motor1.throttle = -speed
        self.motor2.throttle = -speed
        self.motor3.throttle = -speed
        self.motor4.throttle = -speed
        time.sleep(1)

    def goRight(self, speed):
        self.motor1.throttle = -speed
        self.motor2.throttle = speed
        self.motor3.throttle = -speed
        self.motor4.throttle = speed
        time.sleep(1)

    def goLeft(self, speed):
        self.motor1.throttle = speed
        self.motor2.throttle = -speed
        self.motor3.throttle = -speed
        self.motor4.throttle = speed
        time.sleep(1)

    def goright_diagonal(self, speed):
        self.motor1.throttle = 0
        self.motor2.throttle = speed
        self.motor3.throttle = 0
        self.motor4.throttle = speed
        time.sleep(1)

    def goleft_diagonal(self, speed):
        self.motor1.throttle = speed
        self.motor2.throttle = 0
        self.motor3.throttle = speed
        self.motor4.throttle = 0
        time.sleep(1)

    def backright_diagonal(self, speed):
        self.motor1.throttle = -speed
        self.motor2.throttle = 0
        self.motor3.throttle = -speed
        self.motor4.throttle = 0
        time.sleep(1)

    def backleft_diagonal(self, speed):
        self.motor1.throttle = 0
        self.motor2.throttle = -speed
        self.motor3.throttle = 0
        self.motor4.throttle = -speed
        time.sleep(1)

    def turnRight(self, speed):
        self.motor1.throttle = speed
        self.motor2.throttle = -speed
        self.motor3.throttle = -speed
        self.motor4.throttle = speed
        time.sleep(1)

    def turnLeft(self, speed):
        self.motor1.throttle = -speed
        self.motor2.throttle = speed
        self.motor3.throttle = speed
        self.motor4.throttle = -speed
        time.sleep(1)

    def stop(self):
        self.motor1.throttle = 0
        self.motor2.throttle = 0
        self.motor3.throttle = 0
        self.motor4.throttle = 0
        time.sleep(1)
