from picamzero import Camera
from ultralytics import YOLO
from gpiozero import OutputDevice
import time

PICTURE_PATH = "/tmp/current_picture.jpg"
# ze specyfikacji dla Camera Module 3
# https://www.raspberrypi.com/documentation/accessories/camera.html
VERTICAL_FOV = 41 # degrees
HORIZONTAL_FOV = 66 # degrees
CENTER_OFFSET_XY = (0.5, 0.5)

# ze specyfikacji silnika krokowego
# https://botland.store/stepper-motors/3610-stepper-motor-jk42hs40-0504-200-stepsrotations-12v05a043nm-5904422332013.html
ROTATION_RES = 1.8 # degrees

# FIXME do zmiany
MOTOR_X_PIN_ENABLE = OutputDevice(16)
MOTOR_Y_PIN_ENABLE = OutputDevice(17)

cam = Camera()
cam.start_preview()
cam.take_photo(PICTURE_PATH)
cam.stop_preview()

model = YOLO("yolo11n.pt")
result = model(PICTURE_PATH)[0]
xywhn = result.boxes.xywhn
# xywhn zawiera współrzędne znormalizowane (od 0 do 1)
# x = 1 oznacza przesunięcie 0.5*66=33 stopni w prawo
# y = 1 oznacza przesunięcie 0.5*41=20.5 stopni w prawo
diff_x = (xywhn[0] - CENTER_OFFSET_XY[0]) * HORIZONTAL_FOV # degrees
diff_y = (xywhn[1] - CENTER_OFFSET_XY[1]) * VERTICAL_FOV # degrees

steps_x = round(diff_x / ROTATION_RES)
steps_y = round(diff_y / ROTATION_RES)
dir_x = GPIO.HIGH if diff_x >= 0  else GPIO.LOW
dir_y = GPIO.HIGH if diff_y >= 0  else GPIO.LOW
abs_steps_x = abs(steps_x)
abs_steps_y = abs(steps_y)

# obrót x
GPIO.output(MOTOR_X_PIN_ENABLE, GPIO.LOW)
stepper_step(0.001, abs_steps_x, dir_x)
time.sleep(1)
GPIO.output(MOTOR_X_PIN_ENABLE, GPIO.HIGH)

# obrót y
GPIO.output(MOTOR_Y_PIN_ENABLE, GPIO.LOW)
stepper_step(0.001, abs_steps_y, dir_y)
time.sleep(1)
GPIO.output(MOTOR_Y_PIN_ENABLE, GPIO.HIGH)
