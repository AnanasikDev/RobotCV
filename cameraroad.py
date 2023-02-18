# import the necessary packages
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
# import time # Provides time-related functions
import cv2 # OpenCV library
# import math
import numpy as np

from motors import *

from utils import *
from sign import *

from led import *

# Initialize the camera
camera = PiCamera()
 
image_width, image_height = 640, 480

# Set the camera resolution
camera.resolution = (image_width, image_height)
 
# Set the number of frames per second   
camera.framerate = 32
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(image_width, image_height))
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
 
motor_left.forward(normal_speed)
motor_right.forward(normal_speed)

red_sign_observed = False

# Capture frames continuously from the camera
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
     
    # Grab the raw NumPy array representing the image
    image = frame.array[::-1]
    image = np.array(image)
    image[0:2] = [0, 0, 0]
    image[image_height-10:image_height] = [0, 0, 0]
     
    # Display the frame using OpenCV
    cv2.imshow("Frame", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, tr = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV) #175

    cv2.imshow("gray", tr)

    red_mask = load_red_mask(image)

    cv2.imshow("red mask", red_mask)

    img_cvt = tr

    contours, hierarchy = cv2.findContours(tr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    lane = None
    lane_pos = (0, 0)

    for n, cnt in enumerate(contours):
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
        cx = int(cx)
        cy = int(cy)
        radius = int(radius)
        if cy < image_height / 2:
            continue

        m = cv2.moments(cnt)
        m10 = m["m10"]
        m00 = m["m00"]
        m01 = m["m01"]

        area = cv2.contourArea(cnt)
        areaCircle = radius * radius * math.pi
        
        tr = np.float32(tr)
        if area > areaCircle / 40:
            if m00 != 0 and radius > 8 and radius < 100:
                x = int(m10 / m00)
                y = int(m01 / m00)

                if 50 < x < image_width - 50:
                    if y > lane_pos[1]:
                        lane_pos = (x, y)
                        lane = cnt
    
    red = determine_red_sign(red_mask)

    if red_sign_observed and not red:
        red_sign_observed = False
        led_red()
        stop(2)
    if red:
        red_sign_observed = True

    # MOVEMENT

    x, y = lane_pos[0], lane_pos[1]

    cv2.circle(tr, (x, y), 25, (0, 0, 255), 3)

    bottom_screen_point = (image_width / 2, image_height)
    upper_lane_point = (x, y)  # x, y - center of mass

    lane_vector = Vector(bottom_screen_point[0], bottom_screen_point[1], 
                         upper_lane_point[0], upper_lane_point[1])
    up_vector = Vector(0, 1)

    cross_product = up_vector.cross_product(lane_vector)

    k = cross_product / 120
    print(forced_speed + k, k)

    normal_s = clamp(normal_speed, 0, 1)
    forced_s = clamp(forced_speed, 0, 1)

    if cross_product > 0:
        # define as left
        motor_right.forward(forced_s)
        motor_left.forward(normal_s)
        
    else:
        # define as right
        motor_right.forward(normal_s)
        motor_left.forward(forced_s)

    cv2.imshow('contours', tr)
     
    # Wait for keyPress for 1 millisecond
    key = cv2.waitKey(1) & 0xFF
     
    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
     
    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
