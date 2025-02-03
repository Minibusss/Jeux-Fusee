import cv2
import time
import handd as htm
import math


def function():
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)  
    cap.set(4, hCam)
    hand_detector = htm.handDetector(detectionCon=0.7)


    pTime = 0

    success, img = cap.read()
    img = hand_detector.findHands(img)
    lmList = hand_detector.findPosition(img, draw=False)
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]  # doigt 1 (pouce)
        x2, y2 = lmList[20][1], lmList[20][2]  # doigt 2 (index)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Dessine les cercles et la ligne entre les doigts (avec le cercle de moitié)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)  # obtient la longueur entre les doigts
        print(length)
        if length < 50:  # change la couleur du cercle central si doigts collés
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)  # R, V, B (0, 255, 0)


    cTime = time.time()  # (mili)seconde actuelle (epoch linux)
    fps = 1 / (cTime - pTime)  # fps = 1 / (seconde actuelle - seconde précédente)
    pTime = cTime  # met à jour la seconde précédente à chaque affichage d'image
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Img", img)  # montre la video
    return length


function()
