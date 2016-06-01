#-*- coding: utf-8 -*-
# READ BEFORE EDIT!
# HAS TO CHECK THE INDEDENT SETTINGS BEFORE EDIT, IT MAY CAUSE A TROBULE IN INDENTATION PROBLEM. 
# DEFAULT IS 'TWO SPACES' IN EACH INDENT
import cv2
import time
import serial

# Global Parameters
# if the Parameter has underbar in prefix, it is not controlable value. - stil under defining.
# Parameter with prefix "Deprecated_" means it is defined but has never been called, or used.

maxStack = 10 #maximum stacks.
start = 265 # 잘라낼 이미지의 시작라인 - start of the vertical
end = 290   # 잘라낼 이미지의 마지막 라인 - end of the vertical 
threshold = 500 # Maximum value of in gree sign. If the image value exceeds this, the incident is recored in stack
amplificationType = "Multiplication" # Define an operator to amplify image value. "Addition", "Mutiplication" are avaliable. Default is "Multiplication"
# 기준치 산정을 위한 변수 - for what?
# THese variables are doesn't need to be defined as global. It's been used for only 'mux'function.
# What's the meaning of the pre_ on every variable prefix?
_pre_cnt = 0 # it is only used for _threshold, what does 'cnt' stand for ? May be the abbreviation of 'count'.
_pre_max = 0 # it is only used for summation of _maxVal. 
_pre_ave = 0 #


_maxVal = 0  # 현재 최대값 
_threshold = 0 # - for what? 
_threshold_max = 0 # - for what?
_threshold_ave = 0 # - for what?

_stack_cnt = 0 # - for what?



# 검출영역 선택완료 여부
# True : 영역선택 완료 / False : 영역선택이 끝나지 않았음.
_isImageAreaSelected = True # It stores a status of success of the image area which is being selected sucessfully by clicking image area.

# 잘라내기 위한 클릭 제어
# 0 : 기본 상태 / 1 : 임계값 검출중 / 2 : 임계값 검출 / 3 : 영역추출 불량검출 준비완료
_ImageProcessedStatus = 0

# Deprecated_testing_value was used to test. and I forget this var when I delete test code.
# Deprecated_cam_cnt was cnt for cam. But camManager doesn't build. so it's dummy
# Deprecated_Freq, Deprecated_Dur was used to Beep in Window

ser = serial.Serial('/dev/ttyACM0', 115200) # initiailzation of the Arduino


################################# 클래스 정의 #################################################

# 캠 관리 / 미완성
class camManager(): #not yet being used
    cnt = 0
    def __init__(self):
        self.cnt = 0

    def addCam(self):
        self.cnt = self.cnt + 1

    def removeAll(self, cam):
        self.cnt = self.cnt - 1
        del(cam)
        
# 각각의 캠에 대응
class mCam(): 
    cam = None
    s = None
    img = None
    _isImageAreaSelected = True # - what for? in this code?
    def __init__(self, index):
        self.cam = cv2.VideoCapture(index)
        print("%d - Capture start") %index
        self.s = self.cam.read()
        self.img = self.cam.read()
        print("%d - Reading") %index
    def ImageReturn(self):
        return self.img

################################# 함수 정의 #################################################
################################# Global Functions #################################################
# function  :
def valueAmplifier(valueToAmplify, amplificationFeature):
  if amplificationFeature == "Addition":
    return int(valueToAmplify)+int(valueToAmplify)
  else:
    return int(valueToAmplify)*int(valueToAmplify)

# 추후 검출범위를 유동적으로 한다면 해당 함수의 내용을 아래 control_phase함수로 이식할 필요가 있다.
# 영역지정 함수
# 현재 위치를 고정한 상태이기에 사용되지 않는다.
def setArea(event, x, y, flags, param):
  global start, end, _isImageAreaSelected
  global refPt # - for what? this value has never been used in this function. This value has never been delcared from outside.
  if event == cv2.EVENT_LBUTTONDOWN:
    print("is Cllicked %d" %y)
    start = y
    _isImageAreaSelected = False
  elif event == cv2.EVENT_LBUTTONUP:
    print("is Up %d" %y)
    _isImageAreaSelected = True
    end = y

# 마우스 클릭 콜백 함수
def control_phase(event, x, y, flags, param):
  global _ImageProcessedStatus
  if event == cv2.EVENT_LBUTTONDOWN:
    _ImageProcessedStatus = 1 # phase - Thresholds calc
  elif event == cv2.EVENT_RBUTTONDOWN:
    _ImageProcessedStatus = 2 # phase - Thresholds ready

# 시작부터 종류부분까지의 이미지를 잘라낸다
def cropArea(start, end):
  cropped_img = []
  for i in range (int(start), int(end)):
    cropped_line = cam1.img[i]
    cropped_img.append(cropped_line)
  return cropped_img

# 2차원 배열 데이터의 수직값의 합을 지닌 1차원 배열반환
def cumulative(frame_width, start, end, cropped_img):
  cumulative_img = []
  for i in range (0, int(frame_width)):
    c_tmp = 0
    for j in range (0, end-start):
      c_tmp = c_tmp + int(cropped_img[j][i])
    cumulative_img.append(c_tmp)
  return cumulative_img

# 배열길이와 누적값을 토대로 필요한 값 계산
def mux(frame_width, cumulative_img, amplificationFeature):
  global _threshold, _threshold_ave, _threshold_max, _maxVal, _pre_max, _pre_ave, _pre_cnt, _ImageProcessedStatus
  _maxVal = 0
  minVal = 9999
  _threshold = 0
  total = 0 # sumVal -> total

  # step 1
  # 전체 픽셀 중 최대 / 최소값 검출
  for i in range(0, int(frame_width)):
    if _maxVal < cumulative_img[i]:
      _maxVal = int(cumulative_img[i])
    if cumulative_img[i] == 0:
        break
    elif minVal > cumulative_img[i]:
        minVal = int(cumulative_img[i])
        
  # step 2
  # sorry i don't know too
  # HERE, THE NAME OF VARIABLES HAVE TO BE RENAMED SPECIFICALLY. IT IS NOT OBVIOUS WHAT EACH ACTION DOES.
  _maxVal = _maxVal - minVal # Focused on differenciation. 
  # _maxVal = _maxVal * _maxVal # To amplifiy the difference in all mean. - But, I don't still understand why this is done in here. 
  _maxVal = valueAmplifier(_maxVal,amplificationFeature)
  
  # step 3
  # 픽셀값 범위 조정
  for i in range(0, int(frame_width)):
    # 3-1
    # 최소값을 빼는 것으로 수치를 하향조정
    cumulative_img[i] = int(cumulative_img[i]) - minVal #Focused on only differenciation in image value;

    # 3-2
    # 0 미만의 값은 0으로 전환
    if cumulative_img[i] < 0:
      cumulative_img[i] = 0
      
    # 3-3  
    # 제곱을 통해 편차를 늘이고, 이 합과 평균을 검출. 이 평균값을 임계값으로 한다.
    cumulative_img[i] = int(cumulative_img[i]) * int(cumulative_img[i])
    total = total + int(cumulative_img[i]) # - Why here all adding the value of pixel.
  
  # it's not global var   
  average = total/int(frame_width) # - Why here divides the sumVal using image width? SERIOUSELY, I DON'T GET THIS.
  _threshold = average # - for why? Why does the _average pass its value to threshold?

  # 해당 륀에서의 최대값과 평규값의 합을 저장
  if _ImageProcessedStatus == 1:
    #- for why? 아래 3 변수를 따로 저장하게된 이유?
    _pre_max = _pre_max + _maxVal
    _pre_ave = _pre_ave + _average
    _pre_cnt = _pre_cnt + 1
  # 루프 종료를 위해 최종적으로 평균을 계산 후, 전역변수를 0으로 초기화
  elif _ImageProcessedStatus == 2:
    #here just simply can replaced into 
    # _threshold_max = _maxVal/_pre_cnt
    # _threshold_ave = _average/_pre_cnt
    _threshold_max = _pre_max / _pre_cnt
    _threshold_ave = _pre_ave / _pre_cnt
    # 재측정을 위한 초기화
    # - for why?  Why these three variables are defined globaly? These are has been used in this function only. 
    # 아래 3개변수는 이 함수내에서만 사용됨. Global 로 사용하려는 목적은?
    _pre_max = 0
    _pre_ave = 0
    _pre_cnt = 0

    Deprecated_testing_value = int(_threshold_ave * 1) # - what for?
    _ImageProcessedStatus = 3
  return cumulative_img

# 스택 적재
# This function doesn't contains any data.
def stack(result):
  global _stack_cnt
  if result == True: 
      if _stack_cnt < maxStack:
          _stack_cnt = _stack_cnt + 1
  else:
      if _stack_cnt > 0:
          _stack_cnt = _stack_cnt - 1

  
#############################################################################################

cam1 = mCam(0)

frame_width = cam1.cam.get(3) #CV_CAP_PROP_FRAME_WIDTH
frame_height = cam1.cam.get(4) #CV_CAP_PROP_FRAME_HEIGHT - This variable has never been used.

# 디스플레이를 위한 창을 만들고, 클릭처리를 위해 콜백함수 등록
winName = "cam - no.1"
cv2.namedWindow(winName, 1000)
cv2.setMouseCallback(winName,control_phase) # control_phase doesn't return nothing, but why in here?

# s에는 성공/실패여부가, img에는 실제 영상데이터가 담긴다.
# 카메라에 이상이 없다면, 지속적으로 영상을 받아와 처리한다
cam1.s, cam1.img = cam1.cam.read()
print("loop")
while cam1.s: # if cam1.s is in action, value is not null.
  cam1.s, cam1.img = cam1.cam.read()                               

  # 광워 보정을 위해 그레이스케일을 진행
  cam1.img = cv2.cvtColor(cam1.img, cv2.COLOR_RGB2GRAY) # cvtColor, opencv2 function
  
  # 검출영역 주위에 검은색 테두리를 표시
  cv2.rectangle(cam1.img, (0,int(start-1)), (int(frame_width), int(end+1)), (0, 255, 0), 2)
  cv2.imshow(winName, cam1.img)

  # 검출영역이 선택되었음을 확인(2 phase)
  # 현재는 검출영역이 고정되있으므로 항상 참
  if _isImageAreaSelected == True:
    # 선택된 검출영역만을 잘라낸다.
    cropped_img = []
    cropped_img = cropArea(start, end)

    # 수직 라인의 누적값 계산
    cum_img = cumulative(frame_width, start, end, cropped_img)

    # NOY ANY MORE - 값을 제곱하여 편차를 증가
    # Values are amplified due to amplificationType operator.
    cum_img = mux(frame_width, cum_img, amplificationType)
    
    # 범위 지정 && 기준치 측정 완료 후 진행
    # HERE TO FILTER THE VALUE EXCEEDS THE MAXMIUM.
    if _ImageProcessedStatus == 3:
      pre_result = int((_threshold_max - _threshold_ave)*0.001) # - for why? What is this fomula?
      new_result = int((_maxVal - _threshold)*0.001) # - for why? Here also why multiplies by 0.001?
      tmp = new_result - pre_result

      # tmp 값과 임계값을 비교하여 스택의 값을 조절
      if tmp >= threshold:
        stack(True) # problem
      else:
        stack(False)# Okay
        
      # 스택의 적재상태에 따라 아두이노로 신호를 보낸다
      # 1 : LED ON / 2 : LED OFF
      # flag 체크 후 한번씩만 보내도록 하는 if문이 소실. 복구예.....읍읍
      if _stack_cnt >= 10:
        ser.write("1")
      else:
        ser.write("2") 
        
key = cv2.waitKey(10) # 키 입력대기

#  if key != -1:
#      print key
   if key == 27: # ESC : 종료
    cv2.destroyWindow(winName)
    break
  elif key == 32: # maybe P : 10초간 중지
    print "sleep 10 second"
    time.sleep(10)
    print "sleep end"
  elif key == 115:
      _ImageProcessedStatus = 1
  elif key == 101:
      _ImageProcessedStatus = 2
    
print "Goodbye"
del(cam1)
