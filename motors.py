# pin1 = 17
# pin2 = 27
# pin3 = 16
# pin4 = 26

# from gpiozero import Motor
# from time import sleep

# motor1 = Motor(forward=pin1, backward=pin2)

# while True:
#     motor1.forward()
#     sleep(5)
#     motor1.backward()
#     sleep(5)

from gpiozero import Motor
from time import sleep

motor = Motor(forward=27, backward=17)
motor2 = Motor(forward=16, backward=26)

while True:
    motor.forward()
    motor2.forward()
    sleep(5)
    motor2.backward()
    motor.backward()
    sleep(5)