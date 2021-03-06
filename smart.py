import paho.mqtt.client as mqtt
import json
from gpiozero import AngularServo
import math
from secrets import TOKEN

HOSTNAME = "mqtt.beebotte.com"
PORT = 8883
TOPIC = "DogLaser/position"
CACERT = "mqtt.beebotte.com.pem"

min_left_right = 1
max_left_right = 2
left_right_servo = AngularServo(27, min_angle=-45, max_angle=45, min_pulse_width=min_left_right/1000, max_pulse_width=max_left_right/1000)

min_up_down = 0.45
max_up_down = 2.15
up_down_servo = AngularServo(17, min_angle=-90, max_angle=90, min_pulse_width=min_up_down/1000, max_pulse_width=max_up_down/1000)

# center of box is (0, 0)
height = 100
box_size = 30

def point_to_angle(x, y):
    x *= box_size
    y *= box_size
    if x == 0:
        left_right_angle = 0
    else:
        left_right_angle = math.degrees(math.atan(abs(x) / abs(y)))
        if x > 0:
            left_right_angle *= -1

    hyp = math.sqrt(height ** 2 + x ** 2 + y ** 2)
    up_down_angle = -math.degrees(math.acos(height / hyp))

    return left_right_angle, up_down_angle


def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    json_payload = msg.payload.decode('utf-8')
    print(json_payload)

    data = json.loads(json_payload)["data"] 
    split_data = data.split(',')
    x, y = float(split_data[0]), float(split_data[1])

    left_right_angle, up_down_angle = point_to_angle(x, y)
    print(left_right_angle, up_down_angle)

    left_right_servo.angle = left_right_angle
    up_down_servo.angle = up_down_angle

client = mqtt.Client()
client.username_pw_set("token:%s"%TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(CACERT)
client.connect(HOSTNAME, port=PORT, keepalive=60)
client.loop_forever()
