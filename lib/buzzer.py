import RPi.GPIO as GPIO
import time

class BuzzManager:
    buzzer_pin = 11

    def __enter__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        return self

    def buzz(self, pitch=800, duration=0.1):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles) :
            GPIO.output(self.buzzer_pin, True)
            time.sleep(delay)
            GPIO.output(self.buzzer_pin, False)
            time.sleep(delay)

    def __exit__(self, type, value, traceback):
        GPIO.cleanup()
