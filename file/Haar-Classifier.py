import cv2
import matplotlib.pyplot as plt

def empty_array_check(array):
    array = np.asarray(array) # 비어있으면 tuple 로 , 차 있으면 numpy array 로 반환되어서 모두 array 로 바꾸어줌 
    is_empty = array.size == 0 #array 가 비어있으면 is_empty가 true
    return is_empty


def mask_detector(img):
    a=0
    b=0
    face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')
    nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    noses = nose_cascade.detectMultiScale(gray,1.3,5)
    
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
