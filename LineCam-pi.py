#!/usr/bin/env python
import cv2
import time
import numpy as np

# pi specific imports
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
# end of imports

cv2.namedWindow("Output", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Output", cv2.WND_PROP_FULLSCREEN, 1)

# camera
camera = PiCamera()
camera.resolution = (320,240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320,240))
time.sleep(2.5)

# buttons
btn1 = 17
btn2 = 22
btn3 = 23
btn4 = 27
btnShutter = btn1
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(btn1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(btn2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(btn3, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(btn4, GPIO.IN, GPIO.PUD_UP)

# main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # get new frame
    image = frame.array
    # end of new frame

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    lowThreshold = 50
    ratio = 4
    edges = cv2.Canny(gray,lowThreshold,ratio*lowThreshold,apertureSize = 3)
    minLineLength = 4
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    if lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(edges,(x1,y1),(x2,y2),(0,255,0),2)

    cv2.imshow("Edges", edges)
    
    # clear buffer
    rawCapture.truncate(0)
    key = cv2.waitKey(10)
    # end of loop

cv2.destroyWindow("Output")
