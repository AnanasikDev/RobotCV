from gpiozero import LED

red = LED(23)
green = LED(24)

def led_red():
    red.blink(0.2, 0.2, 5)

def led_green():
    green.blink(0.2, 0.2, 5)
