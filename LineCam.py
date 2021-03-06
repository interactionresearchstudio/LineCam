import cv2
import time
import numpy as np

# configuration file
# no configuration file
# end of configuration file

# window
cv2.namedWindow("Output")
# end of window

# camera
capture = cv2.VideoCapture(0)
capture.set(3, 320)
capture.set(4, 240)

if capture.isOpened():
    rval, frame = capture.read()
else:
    rval = False

time.sleep(0.1)
# end of camera

# main loop
while rval:
    # new frame
    rval, frame = capture.read()
    # end of new frame

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
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
    
    # wait for keys
    key = cv2.waitKey(10)
    if key == 27:
        break
    # end of loop

cv2.destroyWindow("Output")
