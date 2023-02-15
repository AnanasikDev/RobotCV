from picamera import PiCamera
camera = PiCamera()
camera.vflip = True
# camera.resolution = (1280, 720)
camera.capture("/home/two/Изображения/img.jpg")

print("Done.")