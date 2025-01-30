import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# variables
width, height = 1200, 720
folderPath = "Presentation"

# camera setup
cap = cv2.VideoCapture(1)
cap.set(3, width)
cap.set(4, height)

# get the list of presentation images
pathImges = sorted(os.listdir(folderPath), key=len)
# print(pathImges)

# variables
imgNumber = 0
hs, ws = int(120 * 1), int(213 * 1)
guestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
annotations = [[]]
annotationNumber = -1
annotationStart = False

# hand detector
detector = HandDetector(detectionCon=0.9, maxHands=1)

while True:
    # import images
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImges[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, guestureThreshold), (width, guestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']

        #  Constarin values for easier drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, w], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal

        # print(fingers)

        if cy <= guestureThreshold:  # if hand is at the height of the face
            annotationStart = False
            # Guesture no 1 - left
            if fingers == [1, 0, 0, 0, 0]:
                annotationStart = False
                print("left")
                if imgNumber > 0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = -1
                    imgNumber -= 1
            # Guesture no 2 - right
            if fingers == [0, 0, 0, 0, 1]:
                annotationStart = False
                print("Right")
                if imgNumber < len(pathImges) - 1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = -1
                    imgNumber += 1

        # Guesture 3 show pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotationStart = False

            # Guesture 4 drawing
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False

        # Guesture -5 Earese
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True
    else:
        annotationStart = False

    # buttonPressed ittereations
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent, annotations[i][j - 1], annotations[i][j], (0, 0, 200), 12)

    # Adding wedcam image on the slides
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws:w] = imgSmall

    # cv2.imshow("image", img)
    cv2.imshow("slides", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
