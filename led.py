from gpiozero import LED
from time import sleep

red = LED(23)
green = LED(24)

while True:
    red.on()
    green.on()
    sleep(0.1)
    red.off()
    green.off()
    sleep(0.1)
