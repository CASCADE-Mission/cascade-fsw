#!/bin/python3
# CASCADE FSW
# CLI

print("Booting...")

from time import time, sleep
from os import system

from mission.vision import fuse_images, initialize_ir_camera, capture_ir_image, initialize_rgb_camera, capture_rgb_image
from mission.servo import probe_deploy, probe_reset

import main

# CONSTANT DEFINITIONS
SERVO_PIN = 17

if __name__ == "__main__":
    # Clear the terminal
    system("clear")

    cmd = ""
    while cmd != "exit":
        cmd = input("CASCADE >> ")

        if cmd == "probe":
            action = input("(r)eset or (d)eploy? ")
            if action == "r":
                probe_reset(SERVO_PIN)
            elif action == "d":
                probe_deploy(SERVO_PIN)
            else:
                continue

        elif cmd == "main":
            action = input("Are you sure? (y/n) ")
            if action == "y":
                main.main()
            else:
                continue

        elif cmd == "clear":
            system("clear")
