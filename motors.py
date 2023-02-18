from gpiozero import Motor

motor_left =  Motor(forward=27, backward=17)
motor_right = Motor(forward=16, backward=26)

normal_speed = 0.6
forced_speed = 1
