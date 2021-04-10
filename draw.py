import signal
import sys

import paho.mqtt.client as mqtt
import json
from gpiozero import AngularServo
import math
from secrets import TOKEN
from time import sleep

from parser import parse

HOSTNAME = "mqtt.beebotte.com"
PORT = 8883
TOPIC = "DogLaser/position"
CACERT = "mqtt.beebotte.com.pem"

min_angle_theta = -45
max_angle_theta = 45
min_pwm_theta = 1/1000
max_pwm_theta = 2/1000
theta_servo = AngularServo(27, min_angle=min_angle_theta, max_angle=max_angle_theta, min_pulse_width=min_pwm_theta, max_pulse_width=max_pwm_theta)

min_angle_phi = -90
max_angle_phi = 90
min_pwm_phi = 0.45/1000
max_pwm_phi = 2.15/1000
phi_servo = AngularServo(17, min_angle=min_angle_phi, max_angle=max_angle_phi, min_pulse_width=min_pwm_phi, max_pulse_width=max_pwm_phi)

# center of box is (0, 0)
x = 100

def sigint_handler(sig, frame):
    print('exiting gracefully')
    set_phi(0)
    set_theta(0)
    sys.exit(0)

def set_phi(angle):
    if angle > 90 or angle < -90:
        raise ValueError('phi out of bounds')
    phi_servo.angle = angle

def set_theta(angle):
    if angle > 45 or angle < -45:
        raise ValueError('theta out of bounds')
    theta_servo.angle = angle

def calculate_phi(y, z):
    phi = math.degrees(math.acos(z / (math.sqrt(x**2 + y**2 + z**2))))
    phi = phi - 90
    return phi

def calculate_theta(y, z):
    if (y == 0):
        return 0
    theta = math.degrees(math.atan(x / y))
    if y < 0:
        theta = -1 * (90 + theta)
        return theta
    theta = 90 - theta
    return theta

def calculate_rho(y, z):
    return math.sqrt(x**2 + y**2 + z**2)

def point_to_angle(y, z):
    return calculate_phi(y, z), calculate_theta(y, z)

def draw_pair(phi, theta):
    try:
        set_phi(phi)
    except:
        print('bad phi: {}'.format(phi))
    try:
        set_theta(theta)
    except:
        print('bad theta: {}'.format(theta))

def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    json_payload = msg.payload.decode('utf-8')
    print(json_payload)
    data = json.loads(json_payload)["data"]
    parsed_data = parse(data)
    
    for i, pair in enumerate(parsed_data):
        #print(i, pair)
        phi, theta = point_to_angle(pair[0], pair[1])
        draw_pair(phi, theta)
        sleep(.05)
    draw_pair(0, 0)

def main():
    signal.signal(signal.SIGINT, sigint_handler)
    client = mqtt.Client()
    client.username_pw_set("token:%s"%TOKEN)
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(CACERT)
    client.connect(HOSTNAME, port=PORT, keepalive=60)
    client.loop_forever()

if __name__ == '__main__':
    main()
