import numpy as np
import cv2
import math

file = "/home/two/Изображения/img.jpg"

img = cv2.imread(file)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, tr = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

tr = 255 - tr

# kernel = np.ones((5, 5), np.uint8)

# img_erosion = cv2.erode(gray, kernel, iterations=1)
# img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)

cv2.imshow("img", tr)
img_cvt = tr

ret, threshold_image = cv2.threshold(img_cvt, 200, 255, cv2.THRESH_BINARY)
# cv2.imshow('threshold ' + file, threshold_image)

contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for n, cnt in enumerate(contours):
    m = cv2.moments(cnt)
    m10 = m["m10"]
    m00 = m["m00"]
    m01 = m["m01"]

    (cx, cy), radius = cv2.minEnclosingCircle(cnt)
    cx = int(cx)
    cy = int(cy)
    radius = int(radius)

    area = cv2.contourArea(cnt)
    areaCircle = radius * radius * math.pi
    
    if area > areaCircle / 10:
        if m00 != 0 and radius > 40 and cy > 400:
            x = int(m10 / m00)
            y = int(m01 / m00)
            print(abs(cx / x), abs(cy / y))
            if 0.98 < abs(cx / x) < 1.02 and\
            0.98 < abs(cy / y) < 1.02:
                cv2.circle(img, (cx, cy), radius, (0, 255, 0), 2)
                cv2.circle(img, (x, y), 10, (0, 0, 255), 3)
    # print(m)
    # if hierarchy[0][n][3] != -1:
    epsilon = 0.001 * cv2.arcLength(cnt, True)
    poly = cv2.approxPolyDP(cnt, epsilon, True)
    cv2.drawContours(img, [poly], -1, (255, 0, 0), 3) #(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    # print(len(poly))


cv2.imshow('contours ' + file, img)

# cv2.imshow("thresh", threshold_image)

cv2.waitKey(0)
