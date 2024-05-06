#!/bin/python3
# CASCADE FSW
# Main executable

print("Booting...")

from time import time, sleep

from mission.vision import fuse_images, initialize_ir_camera, capture_ir_image, initialize_rgb_camera, capture_rgb_image
from mission.servo import probe_deploy, probe_reset

# CONSTANT DEFINITIONS
SERVO_PIN = 17
DROP_DELAY_TIME = 10 # sec
IR_FILTER_INTENSITY = 2 # (deg C)^-1
IR_FILTER_CUTOFF = 15 # deg C
MINIMUM_FEATURE_SIZE = 15 # pixels
SERIAL_PORT = "/dev/ttyACM0"

def error(msg):
    """
    Print an error to the terminal
    """
    print(f"[ERROR] {msg}")

def prompt(msg):
    """
    Prompt the user with a Yes/No question
    """
    raw = input(f"{msg} (y/n) ")

    if raw.lower() in ["y", "yes"]:
        return True
    return False

def main():
    # Start in Safe Mode
    state = "safe"

    while True:
        if state == "safe":
            print("=== Safe Mode ===")

            # Ask if ready to initialize
            if prompt("Configure instrumentation?"):
                state = "prelaunch"
            else:
                print("No action taken")

        elif state == "prelaunch":
            print("Initializing RGB camera...")

            # Set up the RGB camera
            rgb_camera = initialize_rgb_camera()

            print("Initializing IR camera...")

            # Set up the IR camera
            ir_camera = initialize_ir_camera()

            if prompt("Launch?"):
                state = "transit"
            else:
                state = "safe"

        elif state == "transit":
            identified_count = 0

            while True:
                # Take an RGB image
                try:
                    rgb_image = capture_rgb_image(rgb_camera)
                except NameError:
                    error("RGB camera not configured, entering Safe Mode")

                # Take an IR image
                try:
                    ir_image = capture_ir_image(ir_camera, IR_FILTER_INTENSITY, IR_FILTER_CUTOFF)
                except NameError:
                    error("IR camera not configured, entering Safe Mode")

                # Fuse images
                size = fuse_images(rgb_image, ir_image, MINIMUM_FEATURE_SIZE)

                if size is not None:
                    identified_count += 1

                if identified_count >= 20:
                    break

            # Wait
            print(f"Target identified, {DROP_DELAY_TIME} seconds until probe drop")
            sleep(DROP_DELAY_TIME/2)
            print(f"{DROP_DELAY_TIME/2} seconds until probe drop")
            sleep(DROP_DELAY_TIME/2)

            # Drop the probe
            probe_deploy(SERVO_PIN)

            state = "science"

        elif state == "science":
            print("Science Mode :)")
            sleep(5)

        elif state == "eol":
            # Turn on RGB camera
            try:
                rgb_camera.stop()
            except NameError:
                pass

            print("=== EOL ===")

            while True:
                pass

        else:
            # Something's wrong, unrecognized state
            error(f"Spacecraft in unrecognized mode {state}, entering Safe Mode")
            state = "safe"

if __name__ == "__main__":
    main()
