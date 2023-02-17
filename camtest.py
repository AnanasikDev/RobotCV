from picamera import PiCamera
import cv2

camera = PiCamera()
camera.vflip = True
# camera.resolution = (1280, 720)
camera.capture("/home/two/Изображения/img1.jpg")

image = cv2.imread("/home/two/Изображения/img1.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, tr = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)

cv2.imwrite("/home/two/Изображения/img2.jpg", tr)

print("Done.")