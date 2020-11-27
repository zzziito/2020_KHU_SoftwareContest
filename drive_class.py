# -*- coding: utf-8 -*-
from RPi import GPIO
 
class Drive(object):
   def __init__(self, pins):
 
     
       GPIO.setwarnings(False)
       GPIO.setmode(GPIO.BCM)
 
       self.pins = pins
 
       GPIO.setup(self.pins['ENA_1'], GPIO.OUT)
       GPIO.setup(self.pins['IN1_1'], GPIO.OUT)
       GPIO.setup(self.pins['IN2_1'], GPIO.OUT)
       GPIO.setup(self.pins['ENB_1'], GPIO.OUT)
       GPIO.setup(self.pins['IN3_1'], GPIO.OUT)
       GPIO.setup(self.pins['IN4_1'], GPIO.OUT)
       GPIO.setup(self.pins['ENA_2'], GPIO.OUT)
       GPIO.setup(self.pins['IN1_2'], GPIO.OUT)
       GPIO.setup(self.pins['IN2_2'], GPIO.OUT)
       GPIO.setup(self.pins['ENB_2'], GPIO.OUT)
       GPIO.setup(self.pins['IN3_2'], GPIO.OUT)
       GPIO.setup(self.pins['IN4_2'], GPIO.OUT)
 
       self.pwm1 = GPIO.PWM(self.pins['ENA_1'], 50)
       self.pwm2 = GPIO.PWM(self.pins['ENB_1'], 50)
       self.pwm3 = GPIO.PWM(self.pins['ENA_2'], 50)
       self.pwm4 = GPIO.PWM(self.pins['ENB_2'], 50)
 
       self.pwm1.start(50)
       self.pwm2.start(50)
       self.pwm3.start(50)
       self.pwm4.start(50)
  
   def forward(self, speed):
       self.pwm1.ChangeDutyCycle(speed)
       GPIO.output(self.pins['IN1_1'],True)
       GPIO.output(self.pins['IN2_1'],False)
 
       self.pwm2.ChangeDutyCycle(speed)
       GPIO.output(self.pins['IN3_1'],True)
       GPIO.output(self.pins['IN4_1'],False)
 
       self.pwm3.ChangeDutyCycle(speed)
       GPIO.output(self.pins['IN1_2'],True)
       GPIO.output(self.pins['IN2_2'],False)
 
       self.pwm4.ChangeDutyCycle(speed)
       GPIO.output(self.pins['IN3_2'],True)
       GPIO.output(self.pins['IN4_2'],False)
 
   def backward(self, speed):
       self.pwm1.ChangeDutyCycle(speed)
       GPIO.output(self.pins['IN1_1'],False)
       GPIO.output(self.pins['IN2_1'],True)
 
       self.pwm2.ChangeDutyCycle(speed)
       GPIO.output(self.pins['IN3_1'],False)
       GPIO.output(self.pins['IN4_1'],True)
 
       self.pwm3.ChangeDutyCycle(speed)
       GPIO.output(self.pins['IN1_2'],False)
       GPIO.output(self.pins['IN2_2'],True)
 
       self.pwm4.ChangeDutyCycle(speed)
       GPIO.output(self.pins['IN3_2'],False)
       GPIO.output(self.pins['IN4_2'],True)
      
   def left(self):
       self.pwm1.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_1'],False)
       GPIO.output(self.pins['IN2_1'],True)
       self.pwm2.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_1'],True)
       GPIO.output(self.pins['IN4_1'],False)
       self.pwm3.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_2'],True)
       GPIO.output(self.pins['IN2_2'],False)
       self.pwm4.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_2'],False)
       GPIO.output(self.pins['IN4_2'],True)
 
   def right(self):
       self.pwm1.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_1'],True)
       GPIO.output(self.pins['IN2_1'],False)
       self.pwm2.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_1'],False)
       GPIO.output(self.pins['IN4_1'],True)
       self.pwm3.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_2'],False)
       GPIO.output(self.pins['IN2_2'],True)
       self.pwm4.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_2'],True)
       GPIO.output(self.pins['IN4_2'],False)
 
   def leftup_diagonal(self):
       """
       pwm1.ChangeDutyCycle(speed)
       GPIO.output(IN1_1,False)
       GPIO.output(IN2_1,False)
       """
       self.pwm2.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_1'],True)
       GPIO.output(self.pins['IN4_1'],False)
       self.pwm3.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_2'],True)
       GPIO.output(self.pins['IN2_2'],False)
       """
       pwm4.ChangeDutyCycle(speed)
       GPIO.output(IN3_2,False)
       GPIO.output(IN4_2,False)
       """
 
   def rightup_diagonal(self):
       self.pwm1.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_1'],True)
       GPIO.output(self.pins['IN2_1'],False)
       """
       pwm2.ChangeDutyCycle(speed)
       GPIO.output(IN3_1,False)
       GPIO.output(IN4_1,False)
 
       pwm3.ChangeDutyCycle(speed)
       GPIO.output(IN1_2,False)
       GPIO.output(IN2_2,False)
 
       """
       self.pwm4.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_2'],True)
       GPIO.output(self.pins['IN4_2'],False)
 
   def leftdown_diagonal(self):
       self.pwm1.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_1'],False)
       GPIO.output(self.pins['IN2_1'],True)
       """
       pwm2.ChangeDutyCycle(speed)
       GPIO.output(IN3_1,False)
       GPIO.output(IN4_1,False)
       pwm3.ChangeDutyCycle(speed)
       GPIO.output(IN1_2,False)
       GPIO.output(IN2_2,False)
       """
       self.pwm4.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_2'],False)
       GPIO.output(self.pins['IN4_2'],True) 
 
   def rightdown_diagonal(self):
       """
       pwm1.ChangeDutyCycle(speed)
       GPIO.output(IN1_1,False)
       GPIO.output(IN2_1,False)
       """
       self.pwm2.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_1'],False)
       GPIO.output(self.pins['IN4_1'],True)
       self.pwm3.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_2'],False)
       GPIO.output(self.pins['IN2_2'],True)
       """
       pwm4.ChangeDutyCycle(speed)
       GPIO.output(IN3_2,False)
       GPIO.output(IN4_2,False)
       """
   def rightturn(self):
       self.pwm1.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_1'],True)
       GPIO.output(self.pins['IN2_1'],False)
       self.pwm2.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_1'],False)
       GPIO.output(self.pins['IN4_1'],True)
       self.pwm3.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_2'],True)
       GPIO.output(self.pins['IN2_2'],False)
       self.pwm4.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_2'],False)
       GPIO.output(self.pins['IN4_2'],True)
 
   def leftturn(self):
       self.pwm1.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_1'],False)
       GPIO.output(self.pins['IN2_1'],True)
       self.pwm2.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_1'],True)
       GPIO.output(self.pins['IN4_1'],False)
       self.pwm3.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN1_2'],False)
       GPIO.output(self.pins['IN2_2'],True)
       self.pwm4.ChangeDutyCycle(self.speed)
       GPIO.output(self.pins['IN3_2'],True)
       GPIO.output(self.pins['IN4_2'],False)
 
 
# if __name__ == '__main__':
#     pins = {
#         'ENA_1': 1
#     }
#     car = Drive(pins=pins)
