# -*- coding: utf-8 -*-
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')
nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')

def empty_array_check(array):
    array = np.asarray(array) # 비어있으면 tuple 로 , 차 있으면 numpy array 로 반환되어서 모두 array 로 바꾸어줌 
    is_empty = array.size == 0 #array 가 비어있으면 is_empty가 true
    return is_empty

def mask_detector(faces, noses):
    a=0
    b=0

    if empty_array_check (faces) == True: #얼굴이 검출되지 않을 때
        a=1
    else:
        a=0

    if empty_array_check (noses) == True: #코가 검출되지 않을 때
        b=1
    else:
        b=0

    if a==0 and b==1: #얼굴이 검출되고 입이 검출되지 않을 때 
        print("good!")
    elif a==0 and b==0:
        print("put on the mask")
    else:
        print("no face")
	
    return 

def draw_rects(img, faces):    
    for (x,y,w,h) in faces:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    noses = nose_cascade.detectMultiScale(gray,1.3,5)
    mask_detector(faces, noses)
    vis = image.copy()
    draw_rects(vis,faces)
    cv2.imshow("Frame", vis)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)

    if key == ord("q"):
        break
