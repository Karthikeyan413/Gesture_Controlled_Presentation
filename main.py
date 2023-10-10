import cv2 
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np

#variable
width, height = 1280, 720
curPath = os.path.dirname(os.path.abspath(__file__))
folderPath = os.path.join(curPath,"Presentation")

#camera setup
cap = cv2.VideoCapture(0)
#setting width and height to video input
cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

# list of images
Images = sorted(os.listdir(folderPath))
# print(pathImages)

#variables
imgNumber = 0         
hs = int(120*1)
ws = int(213*1)
gestureThreshold = 720
buttonPressed = False
buttonCounter = 0
buttonDelay = 10
annotations = [[]]
annotationNumber = 0
annotationStart = False
thickness = 5
imgCurrent = 'currentSlideImage'
indexFinger = 'indexCoordinates'

#hand detector
detector = HandDetector(detectionCon=0.8,maxHands=1)

def previous_slide():
    global imgNumber, buttonPressed, annotationNumber, annotations, annotationStart
    if imgNumber>0:
        buttonPressed = True
        annotations = [[]]
        annotationNumber = 0
        annotationStart = False
        imgNumber-=1

def next_slide():
    global imgNumber, Images, buttonPressed, annotationNumber, annotations, annotationStart
    if imgNumber < len(Images)-1 :
        buttonPressed = True
        annotations = [[]]
        annotationNumber = 0
        annotationStart = False
        imgNumber+=1

def append_index_to_annotations():
    global annotationNumber, annotations, annotationStart, imgCurrent, indexFinger
    if annotationStart is False:
        annotationStart = True
        annotationNumber += 1
        annotations.append([])
    cv2.circle(imgCurrent,indexFinger,thickness,(0,0,255),cv2.FILLED)
    annotations[annotationNumber].append(indexFinger)

def mark_annotations():
    global annotations, imgCurrent
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent,annotations[i][j-1],annotations[i][j],(0,0,200),12)

while(True):
    #import images
    success, img = cap.read()
    img = cv2.flip(img,1)

    pathFullImg = os.path.join(folderPath,Images[imgNumber])
    imgCurrent = cv2.imread(pathFullImg)
    imgCurrent = cv2.resize(imgCurrent,(width,height))

    hands, img = detector.findHands(img)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']
        # print(fingers)

        lmList = hand['lmList']
        #constrain values
        # xVal = int(np.interp(lmList[8][0],[width//2,w],[0,width]))
        # yVal = int(np.interp(lmList[8][1],[150,height-150],[0,height]))
        indexFinger = lmList[8][0]*2,lmList[8][1]*2
        #1 move left
        if fingers == [1,0,0,0,0]:
            previous_slide()
        #2 move right
        if fingers == [0,0,0,0,1]:
            next_slide()
        #3 pointer
        if fingers == [0,1,0,0,0]:
            annotationStart = False
            cv2.circle(imgCurrent,indexFinger,thickness,(0,0,255),cv2.FILLED)
        #4 draw
        if fingers == [0,1,1,0,0]:
            append_index_to_annotations()
        else:
            annotationStart = False
        #5 erase
        if fingers == [0,1,1,1,0]:
            if annotations:
                if annotationNumber >= 0 :        
                    annotations.pop(-1)
                    annotationNumber -= 1
                    buttonPressed = True
    else:
        annotationStart = False
    #Button Pressed Iterations
    if buttonPressed:
        buttonCounter += 1 
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    mark_annotations()

    #adding webcam images on the slide
    imgSmall = cv2.resize(img,(ws,hs))
    h,w,_ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall
    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)    
    
    
    
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break