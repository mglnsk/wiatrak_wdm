import wiatrak
import time
from ultralytics import YOLO
from picamzero import Camera
from motor import StepperMotor

def main():
    print("wiatrak-wdm starting")

    cam = Camera()
    model = YOLO("yolo11n.pt")
    motor_x = StepperMotor(0, 1, 2)
    motor_y = StepperMotor(3, 4, 5)

    while True:
        wiatrak.main_loop(cam, model, motor_x, motor_y)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
