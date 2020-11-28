# 마스크 미착용자 추적 로봇 
이것은 [경희대학교](https://www.khu.ac.kr/kor/main/index.do) [ICNS 연구실](http://ce.khu.ac.kr/index.php?hCode=GRADUATE_03_01_13)에서 주최하는 [2020 제 1회 공개 SW 활용 공모전](https://ibb.co/G5F3HMd)을 위한 소프트웨어입니다. 

## Table of Contents

  
  
## 프로젝트 개요 
 
코로나19 바이러스 대유행이 장기화되는 가운데, 마스크를 착용하는 것은 가장 간단하고도 효과적인 생활 방역입니다. 특히 공공시설에서의 마스크 착용은 대규모 감염이 일어나지 않도록 막아줍니다. ([파주 스타벅스](https://www.chosun.com/site/data/html_dir/2020/08/19/2020081904509.html)) 사회적 거리두기 단계에 따라 정부에서 마스크 착용을 강제하고 있지만, 때때로 출몰하는 '[노마스크 빌런](https://imnews.imbc.com/original/mbig/5947162_29041.html)'은 우리를 불안하게 합니다. 특히나 백화점같은 다중 이용 시설에서 말이죠.  
"마스크 써주세요" 라고 직접 이야기하자니 되려 해코지 당하거나 침이 튈까봐 무서우신 분들, 혹은 넓은 실내공간에서 상시 마스크 미착용자를 단속하기 어려운 상황에 필요한 소프트웨어를 제안합니다. 

### 기능 

  + 마스크 미착용자 판별 후 졸졸 따라다니기
  + 따라다니며 사이렌을 울리고 마스크 착용 안내 멘트 송출
  + 기본적인 실내 주행 알고리즘 (장애물 피하기)
  
<img width="300" alt="스크린샷 2020-10-03 오후 10 10 07" src="https://user-images.githubusercontent.com/52185595/99485785-805fbd00-29a6-11eb-9565-5bd02028d220.png">

### 준비물

#### Hardware

+ **Raspberry Pi 4 Model B** : 동영상 처리, 메카넘휠 구동, 로봇팔 구동
+ **L298N** : 모터 드라이버
+ **PCA9685** : 여러 대의 모터 구동을 위한 모듈
+ **Lidar** 
+ **Mechanum wheel**
+ **Picam** : 촬영해서 라즈베리파이로 보내기 
+ **Robot Arm** : 마스크 집기 

라즈베리파이 Python 코딩을 위한 기본 세팅은 [여기](https://opencv.org/)

#### Software

+ **PYTHON** with Opencv 

## 주행 알고리즘 

기본적으로는 <마스크 안 쓴 얼굴을 찾은 후 따라간다> 는 논리입니다. 그러기 위해서 우선 얼굴을 찾고, 마스크를 썼냐 안 썼냐를 판별하는 프로그램을 만들었습니다. 

### 얼굴 인식

#### 하르 분류기 Haar-Classifier

영상 처리를 위한 파이썬 라이브러리인 [OpenCV](https://opencv.org/) 에서는 특징점 검출을 통한 분류기가 있습니다. 그 중 Haar Classifier 은 특정 형태의 물체를 찾고자 할 때 사용할 수 있는 대표적인 방법 중 하나입니다. 이는 특징(feature)을 기반으로 오브젝트를 검출하고, 특징은 직사각형 영역으로 구성되어 있기 때문에 픽셀을 직접 사용할 때보다 동작 속도가 빠릅니다. 
하르 분류기는 다음과 같이 사용할 수 있습니다. (깃헙 내 폴더 files 에 xml 파일을 첨부해 놓았습니다.)

```python
img = cv2.imread('face.jpeg')
face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray,1.3,5)
for (x,y,w,h) in faces:
    final_img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
plt.imshow(final_img)
```
![2](https://user-images.githubusercontent.com/52185595/100444846-7e58d500-30ef-11eb-8b80-3423f333cbdd.png)

특징은 Edge, Line, Four-rectangle 세 가지로 분류할 수 있습니다. 이때 얼굴 검출을 하는데 의미있는 특징을 골라내서 오브젝트를 인식합니다. 

<img width="400" alt="md_27" src="https://user-images.githubusercontent.com/52185595/100446236-c842ba80-30f1-11eb-9fff-bd3000faa114.png">

하르 분류기를 사용하면 얼굴 뿐 아니라 눈, 입, 코 등도 검출할 수 있습니다. 때문에 

*얼굴이 보이는데 코가 안 보인다 -> 마스크를 썼다* 

라는 [코드](https://github.com/zzziito/2020_KHU_SoftwareContest/blob/main/files/Haar-Classifier.py)를 작성했습니다. 

<img width="400" alt="md_27" src="https://user-images.githubusercontent.com/52185595/100448706-0fcb4580-30f6-11eb-8248-6d56c427be67.jpg">

위와 같이 밝고 선명한 이미지에서는 잘 작동하는 것을 볼 수 있습니다. 하지만 라즈베리파이 Video Streaming 에서는 전혀 작동하지 않았습니다. 

![1](https://user-images.githubusercontent.com/52185595/100450260-abf64c00-30f8-11eb-8b88-e9ee720253a6.gif)

![5](https://user-images.githubusercontent.com/52185595/100453635-a26fe280-30fe-11eb-99e7-86f6381eda1c.jpg)



[라즈베리파이 카메라 라이브 스트리밍 코드](https://github.com/zzziito/2020_KHU_SoftwareContest/blob/main/files/videoStreaming.py)

[하르 분류기를 이용한 Real Time Face Detection 코드](https://github.com/zzziito/2020_KHU_SoftwareContest/blob/main/files/videoStreaming_HaarClassifier.py)



*Haar - Classifier 참조*
***

<https://darkpgmr.tistory.com/70>

<https://webnautes.tistory.com/1352>

<https://m.blog.naver.com/zeta0807/221304976623>


+ 제공해주신 카메라를 쓰지 않은 이유는, PiCam 에 비해 스트리밍 속도가 너무 느리기 때문이었습니다. 

![4](https://user-images.githubusercontent.com/52185595/100461328-01882400-310c-11eb-9eb0-45b3ad60d524.gif)

위 영상을 보면, PiCam 은 스트리밍할 때 딜레이가 거의 없지만, Usb 연결을 하는 웹캠은 1초정도 딜레이가 발생합니다. 1초나 딜레이가 발생하면 주행이 거의 불가능하다고 판단했습니다. 



#### Real Time Face Mask Detection with Opencv, Keras and Deep Learning

그래서 [이곳](https://github.com/chandrikadeb7/Face-Mask-Detection) 을 참고해 딥러닝을 이용해 마스크를 판별했습니다. 

[코드](https://github.com/zzziito/2020_KHU_SoftwareContest/blob/main/files/DeepLearning_Streaming.py)

![6](https://user-images.githubusercontent.com/52185595/100456142-39d73480-3103-11eb-94d4-b530b3485aab.jpg)

![3](https://user-images.githubusercontent.com/52185595/100455599-4a3adf80-3102-11eb-81ae-85244d4a6138.gif)

위와 같이 어느 상황에서도 얼굴을 잘 인식하며, 대략 2m 떨어진 곳까지 인식이 가능했습니다. 

<img width="400" alt="md_27" src="https://user-images.githubusercontent.com/52185595/100456852-5a53be80-3104-11eb-99ec-00e25c13ee23.jpg">

위와 같이 화면을 세 개의 section 으로 나누어서 얼굴이 어느 section에 위치하느냐에 따라 모터를 작동시키는 알고리즘으로 사람을 추적합니다. 

### 모터 동작

주최 측에서 제공해주신 물품은 라즈베리파이와 [STM32F407G-DISC1](https://www.st.com/en/evaluation-tools/stm32f4discovery.html) 이지만, 여러 개의 GPIO 핀을 사용할 수 있게 해 주는 모듈 
pca9685 를 발견하고 , 굳이 STM 보드를 사용할 필요가 없다고 느껴 사용하지 않았습니다. 

[pca9685 를 사용하지 않고 코딩하기 ! - 모터를 쪼금만 사용할 때](https://github.com/zzziito/2020_KHU_SoftwareContest/blob/main/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B4%20%EB%AA%A8%ED%84%B0%20%EC%BB%A8%ED%8A%B8%EB%A1%A4.md)


<img width="300" alt="8" src="https://user-images.githubusercontent.com/52185595/100461788-99860d80-310c-11eb-887f-dfda450376c2.png">


[pca9685 데이터시트](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-16-channel-servo-driver-with-raspberry-pi.pdf)

다음과 같이 연결해줍니다. 

<img width="400" alt="md_27" src="https://user-images.githubusercontent.com/52185595/100461981-e5d14d80-310c-11eb-8176-31006d446c9f.png">

불러와야 하는 모듈, duty cycle, PWM 에 관한 사전 설정 및 주행 명령을 담은 클래스인 drivingclass 를 만들고 불러옵니다. 

[drive_class](https://github.com/zzziito/2020_KHU_SoftwareContest/blob/main/drive_class.py)

```python
from drive_class import drivingclass
car = drivingclass()
car.goForward(1)
```
다음과 같이 사용이 가능합니다. 

![5](https://user-images.githubusercontent.com/52185595/100463351-0b5f5680-310f-11eb-8998-90b8017b433a.gif)

### 라이다

<img width="250" alt="9" src="https://user-images.githubusercontent.com/52185595/100490452-d8dd4a00-315e-11eb-817c-9d5ccac5023a.png">

[YDLidar X4](https://www.ydlidar.com/products/view/5.html)

[이 사이트](https://pypi.org/project/PyLidar3/) 를 참고하여 PyLidar3 패키지를 이용했습니다. ([라이다 세팅 및 오류 해결 방법은 여기](https://pypi.org/project/PyLidar3/)) 
깃허브의 /Examples/LidarTest.py 를 실행하면 다음과 같은 generator 가 출력됩니다. 

![12](https://user-images.githubusercontent.com/52185595/100490941-3378a500-3163-11eb-8410-f10e7ec25926.png)





## 로봇 팔 










 


