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

#### Software

+ **PYTHON** with Opencv 

## 주행 알고리즘 

기본적으로는 <마스크 안 쓴 얼굴을 찾은 후 따라간다> 는 논리입니다. 그러기 위해서 우선 얼굴을 찾고, 마스크를 썼냐 안 썼냐를 판별하는 프로그램을 만들었습니다. 

### 얼굴 인식

#### 하르 분류기 Haar-Classifier

영상 처리를 위한 파이썬 라이브러리인 [OpenCV](https://opencv.org/) 에서는 특징점 검출을 통한 분류기가 있습니다. 그 중 Haar Classifier 은 특정 형태의 물체를 찾고자 할 때 사용할 수 있는 대표적인 방법 중 하나입니다. 이는 특징(feature)을 기반으로 오브젝트를 검출하고, 특징은 직사각형 영역으로 구성되어 있기 때문에 픽셀을 직접 사용할 때보다 동작 속도가 빠릅니다. 
하르 분류기는 다음과 같이 사용할 수 있습니다. 

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





## 로봇 팔 










 


