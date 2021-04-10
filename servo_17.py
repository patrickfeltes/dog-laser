from gpiozero import AngularServo
from time import sleep

min_num = 0.45
max_num = 2.15
left_right_servo = AngularServo(17, min_angle=-90, max_angle=90, min_pulse_width=min_num/1000, max_pulse_width=max_num/1000)

while True:
    # s.angle = angle

    setting = input("Enter an angle: ")
    left_right_servo.angle = int(setting)
    #if setting == 'max':
    #    s.max()

    #if setting == 'mid':
    #    s.mid()

    #if setting == 'min':
    #    s.min()

