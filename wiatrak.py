from picamzero import Camera
from ultralytics import YOLO
import time
from motor import StepperMotor


PICTURE_PATH = "/tmp/current_picture.jpg"
# ze specyfikacji dla Camera Module 3
# https://www.raspberrypi.com/documentation/accessories/camera.html
VERTICAL_FOV = 41 # degrees
HORIZONTAL_FOV = 66 # degrees
CENTER_OFFSET_XY = (0.5, 0.5)

# ze specyfikacji silnika krokowego
# https://botland.store/stepper-motors/3610-stepper-motor-jk42hs40-0504-200-stepsrotations-12v05a043nm-5904422332013.html
ROTATION_RES = 1.8 # degrees

def main_loop(cam, model, motor_x, motor_y):
    cam.start_preview()
    cam.take_photo(PICTURE_PATH)
    cam.stop_preview()


    result = model(PICTURE_PATH)[0]
    xywhn = result.boxes.xywhn
    # xywhn zawiera współrzędne znormalizowane (od 0 do 1)
    # x = 1 oznacza przesunięcie 0.5*66=33 stopni w prawo
    # y = 1 oznacza przesunięcie 0.5*41=20.5 stopni w prawo
    diff_x = (xywhn[0] - CENTER_OFFSET_XY[0]) * HORIZONTAL_FOV # degrees
    diff_y = (xywhn[1] - CENTER_OFFSET_XY[1]) * VERTICAL_FOV # degrees

    steps_x = round(diff_x / ROTATION_RES)
    steps_y = round(diff_y / ROTATION_RES)
    dir_x = int(diff_x >= 0)
    dir_y = int(diff_y >= 0)
    abs_steps_x = abs(steps_x)
    abs_steps_y = abs(steps_y)

    # obrót x
    if abs_steps_x >= 2:
        motor_x.driver_enable()
        motor_x.stepper_step(0.001, abs_steps_x, dir_x)
        time.sleep(1)
        motor_x.driver_disable()

    # obrót y
    if abs_steps_y >= 2:
        motor_y.driver_enable()
        motor_y.stepper_step(0.001, abs_steps_y, dir_y)
        time.sleep(1)
        motor_y.driver_disable()
