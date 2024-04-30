from gpiozero import Servo
from time import sleep

def servo_deploy():
    servo = Servo(17)
    sleep(0.5)
    servo.max()
    sleep(0.5)

def servo_reset():
    servo = Servo(17)
    sleep(0.5)
    servo.min()
    sleep(0.5)

