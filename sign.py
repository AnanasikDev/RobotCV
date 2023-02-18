import cv2
import numpy as np

def load_red_mask(image):
    img = image.transpose(1, 0, 2)[0:image.shape[0]//3*2:].transpose(1, 0, 2)[0:image.shape[0]//3*2]
    image_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower = np.array([166, 173, 200])
    # upper = np.array([175, 255, 255])

    lower = np.array([162, 162, 0])
    upper = np.array([175, 255, 255])

    # lower = np.array([157, 199, 0])
    # upper = np.array([179, 255, 255])

    mask = cv2.inRange(image_hsv, lower, upper)
    final_img = cv2.bitwise_and(img, img, mask=mask)
    return final_img


def determine_red_sign(image):
    img_cvt = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(img_cvt, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for n, cnt in enumerate(contours):
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        poly = cv2.approxPolyDP(cnt, epsilon, True)
        cv2.drawContours(image, [poly], -1, (0, 0, 255), 3)
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        x, y, radius = int(x), int(y), int(radius)
        # if radius > 50 and radius < 90:
        if radius > 35 and radius < 110:
            cv2.circle(image, (x, y), radius, (0, 255, 0), 3)
            print("STOP")
            return True
    
    return False


# hsv min max: 166 173 200 175 255 255
# rgb: 116, 8, 31 = hsv: 347, 93, 45 | hsv min max: 157, 199, 0, 179, 255, 255