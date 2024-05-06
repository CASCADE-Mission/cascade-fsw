from gpiozero import Servo
from time import sleep

def probe_reset(pin):
    servo = Servo(pin)
    sleep(0.5)
    servo.max()
    sleep(0.5)

def probe_deploy(pin):
    servo = Servo(pin)
    sleep(0.5)
    servo.min()
    sleep(0.5)

