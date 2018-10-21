# Gets number of red pixels, and saves frame when number is sufficiently high

import cv2
import numpy as np

cap = cv2.VideoCapture('video3.m4v')

while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Idle values:
    # [100, 21, 180]
    # [255, 255, 200]

    lower_red = np.array([100, 0, 160])
    upper_red = np.array([255, 255, 205])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    count = 0

    #for x in np.nditer(mask):
        #if(x > 1):
            #count = count + 1

    #cv2.putText(frame, str(count), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
    #count = 0

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
