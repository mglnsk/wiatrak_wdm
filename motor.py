from gpiozero import OutputDevice
import time

class StepperMotor():
    def __init__(self, pin_enable, pin_direction, pin_step):
        self.pin_enable = OutputDevice(pin_enable)
        self.pin_direction = OutputDevice(pin_direction)
        self.pin_step = OutputDevice(pin_step)

    def driver_enable(self):
        self.pin_enable.value = 0

    def driver_disable(self):
        self.pin_enable.value = 1

    def _stepper_step(self, delay, steps, direction):
        self.pin_direction.value = direction
        for _ in range(steps):
            self.pin_step = 1
            time.sleep(delay)
            self.pin_step = 0
            time.sleep(delay)

    def step(self, steps, direction):
        self.driver_enable()
        self._stepper_step(0.001, steps, direction)
        time.sleep(1)
        self.driver_disable()
