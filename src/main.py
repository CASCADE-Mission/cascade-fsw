#!/bin/python3
# CASCADE FSW
# Main executable

print("Configuring...")

from mission.vision import fuse_images, initialize_ir_camera, capture_ir_image, initialize_rgb_camera, capture_rgb_image

# CONSTANT DEFINITIONS

SERVO_PIN = 17

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

if __name__ == "__main__":
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
            identified_target = False

            while not identified_target:
                # Take an RGB image
                try:
                    rgb_image = capture_rgb_image(rgb_camera)
                except NameError:
                    error("RGB camera not configured, entering Safe Mode")

                # Take an IR image
                try:
                    ir_image = capture_ir_image(ir_camera)
                except NameError:
                    error("IR camera not configured, entering Safe Mode")

                # Fuse images
                fused = fuse_images(rgb_image, ir_image)

                if not prompt("Continue?"):
                    state = "eol"
                    break

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
