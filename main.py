import wiatrak
import time
from ultralytics import YOLO
from picamzero import Camera
from motor import StepperMotor
from gpiozero import Motor

from threading import Thread
from flask import Flask, request, jsonify
from conf import FAN_SPEED, CENTER_OFFSET_XY

app = Flask(__name__)

@app.route('/configure', methods=['POST'])
def configure():
    data = request.get_json()
    if 'center_offset' in data:
        global CENTER_OFFSET_XY
        CENTER_OFFSET_XY = tuple(data['center_offset'])
    if 'fan_speed' in data:
        global FAN_SPEED
        FAN_SPEED = float(data['fan_speed'])
    return jsonify({"status": "success"}), 200

@app.route("/")
def index():
    return "Fan control server"

def fan():
    cam = Camera()
    model = YOLO("yolo11n.pt")
    motor_x = StepperMotor(0, 1, 2) # A4988 pins
    motor_y = StepperMotor(3, 4, 5) # A4988 pins

    motor_dc = Motor(6, 7) # L298n pins

    while True:
        wiatrak.main_loop(cam, model, motor_x, motor_y, motor_dc)
        time.sleep(0.1)


if __name__ == '__main__':
    print("wiatrak-wdm starting")
    Thread(target=fan, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)
