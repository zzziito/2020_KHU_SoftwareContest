# -*- coding: utf-8 -*-
from RPi import GPIO
import time
from time import sleep
import sys, tty, termios
 
from driving_class import Drive
 
#ENA_1 = 전륜 왼쪽 바퀴
#ENB_1 = 전륜 오른쪽 바퀴
#ENA_2 = 후륜 왼쪽 바퀴
#ENB_2 = 후륜 오른쪽 바퀴
 
def getch():
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
       tty.setraw(sys.stdin.fileno())
       ch = sys.stdin.read(1)
   finally:
       termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch
 
pins = {
   'ENA_1': 4,
   'IN1_1': 17,
   'IN2_1': 18,
 
   'ENA_2': 13,
   'IN3_1': 24,
   'IN4_1': 25,
  
   'ENB_1': 23,
   'IN1_2': 19,
   'IN2_2': 26,
 
 
   'ENB_2': 21,
   'IN3_2': 20,
   'IN4_2': 16,
}
 
 
car = Drive(pins=pins)
 
 
while True:
   char = getch()
  
   if(char == "w"):
       print("leftup_diagonal")
       car.leftup_diagonal()
       time.sleep(1)
   if(char == "e"):
       print("forward")
       car.forward()
       time.sleep(2)
   if(char == "r"):
       print("rightup_diagonal")
       car.rightup_diagonal()
       time.sleep(1)
   if(char == "s"):
       print("left")
       car.left()
       time.sleep(1)
   if(char == "d"):
       print("Program ended")
       break
   if(char == "f"):
       print("right")
       car.right()
       time.sleep(1)
   if(char == "x"):
       print("leftdown_diagonal")
       car.leftdown_diagonal()
       time.sleep(1)
   if(char == "c"):
       print("backward")
       car.backward()
       time.sleep(1)
   if(char == "v"):
       print("rightdown_diagonal")
       car.rightdown_diagonal()
       time.sleep(1)
 
char = ""
 
 
# car.leftup_diagonal()
# time.sleep(2)
# car.rightdown_diagonal()
# time.sleep(2)
 
GPIO.cleanup()
