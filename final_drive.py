# -*- coding: utf-8 -*-

# 주행용
# from RPi import GPIO
import time
from time import sleep
import sys
import tty
import termios
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor

from drive_class import drivingclass

# 마스크 인식용

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os

# 라이다용

import PyLidar3
port = "/dev/ttyUSB0"
Obj = PyLidar3.YdLidarX4(port)

# 주행용 기본세팅

car = drivingclass()

# 마스크 인식용 기본세팅


def detect_and_predict_mask(frame, faceNet, maskNet):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))
    faceNet.setInput(blob)
    detections = faceNet.forward()
    faces = []
    locs = []
    preds = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > args["confidence"]:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)
            faces.append(face)
            locs.append((startX, startY, endX, endY))
    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)
    return (locs, preds)


ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
                default="face_detector",
                help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
                default="mask_detector.model",
                help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
                                "res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

print("[INFO] loading face mask detector model...")
maskNet = load_model(args["model"])

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# 사용 변수 선언

box = []
face_max = 150

# 시작!
if(Obj.Connect()):
    gen = Obj.StartScanning()
    print("Lidar Started Working")
    while True:

        # 일반 주행 / 얼굴인식 주행 구분하여 시행
        mask_detected = 0

        # 라이다 값 받아오기
       
        lidar_set = set()
        data = next(gen)
        lidar_stop = 0
        for angle in range(0, 20):  # 0~20도까지 거리 평균 내서 distance 에 저장
            lidar_set.add(data[angle])
        for angle in range(340, 359):
            lidar_set.add(data[angle])
        distance = sum(lidar_set) // len(lidar_set)
        print(distance)
        if distance < 500:
            lidar_stop = 1  # lidar_stop 이 1 이 되면 멈춰야 함

        # 실시간 스트리밍 시작 & 화면 크기 정보 받아오기
        frame = vs.read()
        frame = imutils.resize(frame)
        height, width = frame.shape[:2]
        horizontal_1 = width//3
        horizontal_2 = (width//3)*2

        # 화면에 가이드 선 긋기
        frame = cv2.line(frame, (horizontal_1, 0),
                         (horizontal_1, height), (255, 0, 0), 1)
        frame = cv2.line(frame, (horizontal_2, 0),
                         (horizontal_2, height), (255, 0, 0), 1)
        section = 0

        # Mask Prediction 부분
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        cv2.imshow("Frame", frame)

        if box:
            mask_detected = 1
            print("mask_detected ==1, driving mode change")

        # box 안에 Face위치 정보 들어있음.

        if mask_detected == 0:
            car.goForward(0.5)
            print("normal drive mode")
            if lidar_stop == 1:
                car.turnLeft(0.5)  # 앞에 장애물 있을 경우 왼쪽으로 돌기
                print("there is something in front of me")
                timez.sleep(1)

        elif mask_detected == 1:  # 마스크 인식주행 시작
            center_x = (box[0]+box[2])/2
            box_size = box[2]-box[0]
            if center_x <= horizontal_1:
                section = 1
            elif center_x > horizontal_1 and center_x <= horizontal_2:
                section = 2
            else:
                section = 3

            if section == 3 and box_size < 120:
                car.goRight(0.6)
                print("car Go Right")
            elif section == 2 and box_size < 120:
                car.goForward(0.6)
                print("car Go Forward")
            elif section == 1 and box_size < 120:
                car.goLeft(0.6)
                print("car Go Left")
            elif section == 1 and box_size >= 120:
                car.stop()
            elif section == 2 and box_size >= 120:
                car.stop()
            elif section == 3 and box_size >= 120:
                car.stop()

        else:
            car.stop()

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            car.stop()
            break
    cv2.destroyAllWindows()
    vs.stop()
else:
    print("Error connecting to device")
