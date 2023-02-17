# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import math
import numpy as np

# Initialize the camera
camera = PiCamera()
 
# Set the camera resolution
camera.resolution = (640, 480)
 
# Set the number of frames per second   
camera.framerate = 32
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(640, 480))
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
 
# Capture frames continuously from the camera
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
     
    # Grab the raw NumPy array representing the image
    image = frame.array[::-1]
    # image = np.float32(image)
     
    # Display the frame using OpenCV
    cv2.imshow("Frame", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, tr = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    cv2.imshow("gray", tr)

    
    #tr = 255 - tr
    #img_cvt = tr
    img_cvt = tr

    ret, threshold_image = cv2.threshold(img_cvt, 200, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for n, cnt in enumerate(contours):
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
        cx = int(cx)
        cy = int(cy)
        radius = int(radius)
        if cy < 400:
            continue

        m = cv2.moments(cnt)
        m10 = m["m10"]
        m00 = m["m00"]
        m01 = m["m01"]

        area = cv2.contourArea(cnt)
        areaCircle = radius * radius * math.pi
        
        tr = np.float32(tr)
        if area > areaCircle / 30:
            if m00 != 0 and radius > 10:
                x = int(m10 / m00)
                y = int(m01 / m00)
                #if x 
                #print(abs(cx / x), abs(cy / y))
                
        #if 0.98 < abs(cx / x) < 1.02 and\
        #   0.98 < abs(cy / y) < 1.02:
                cv2.circle(tr, (cx, cy), radius, (0, 255, 0), 2)
                cv2.circle(tr, (x, y), 10, (0, 0, 255), 3)
        # print(m)
        # if hierarchy[0][n][3] != -1:

        #epsilon = 0.001 * cv2.arcLength(cnt, True)
        #poly = cv2.approxPolyDP(cnt, epsilon, True)
        #cv2.drawContours(image, [poly], -1, (255, 0, 0), 3)
        """
        image = np.float32(image)
        epsilon = 0.001 * cv2.arcLength(cnt, True)
        poly = cv2.approxPolyDP(cnt, epsilon, True)
        cv2.drawContours(image, [poly], -1, (255, 0, 0), 3)""" #(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # print(len(poly))

    cv2.imshow('contours', tr)
     
    # Wait for keyPress for 1 millisecond
    key = cv2.waitKey(1) & 0xFF
     
    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
     
    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break