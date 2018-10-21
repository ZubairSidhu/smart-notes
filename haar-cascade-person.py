import numpy as np
import imutils
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
#https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_upperbody.xml
body_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')

capture = cv2.VideoCapture('video2.m4v')

while 1:
    ret, img = capture.read()
    img = imutils.resize(img, width=min(300, img.shape[1]))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    body = body_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in body:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
