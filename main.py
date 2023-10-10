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
cap.set(3,width)
cap.set(4,height)

# list of images
pathImages = sorted(os.listdir(os.path.join(os.curdir,folderPath)),key=len)
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

#hand detector
detector = HandDetector(detectionCon=0.8,maxHands=1)

while(True):
    #import images
    success, img = cap.read()
    img = cv2.flip(img,1)

    pathFullImg = os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImg)
    imgCurrent = cv2.resize(imgCurrent,(width,height))

    hands, img = detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),5)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']
        # print(fingers)

        lmList = hand['lmList']
        #constrain values
        xVal = int(np.interp(lmList[8][0],[width//2,w],[0,width]))
        yVal = int(np.interp(lmList[8][1],[150,height-150],[0,height]))
        indexFinger = xVal,yVal

        if(cy <= gestureThreshold):
            # annotationStart = False
            #1 move left
            if fingers == [1,0,0,0,0]:
                if imgNumber>0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    annotationStart = False
                    imgNumber-=1
            #2 move right
            if fingers == [0,0,0,0,1]:
                if imgNumber < len(pathImages)-1 :
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    annotationStart = False
                    imgNumber+=1
            #3 pointer
            if fingers == [0,1,0,0,0]:
                annotationStart = False
                cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)
            #4 draw
            if fingers == [0,1,1,0,0]:
                if annotationStart is False:
                    annotationStart = True
                    annotationNumber += 1
                    annotations.append([])
                cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)
                annotations[annotationNumber].append(indexFinger)
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

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent,annotations[i][j-1],annotations[i][j],(0,0,200),12)

    #adding webcam images on the slide
    imgSmall = cv2.resize(img,(ws,hs))
    h,w,_ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall
    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)    
    
    
    
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break