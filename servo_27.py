from gpiozero import AngularServo
from time import sleep

min_up_down = 1
max_up_down = 2
up_down_servo = AngularServo(27, min_angle=-45, max_angle=45, min_pulse_width=min_up_down/1000, max_pulse_width=max_up_down/1000)

while True:
    setting = input("Enter an angle: ")
    up_down_servo.angle = int(setting)

