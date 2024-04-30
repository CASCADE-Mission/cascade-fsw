# CASCADE FSW
# Computer Vision

import time
import sys

import cv2
import numpy as np
from picamera2 import Picamera2

import amg8833_i2c

BLUE_MASK1 = (
    np.array([300, 60, 60]),
    np.array([360, 255, 255]),
)

BLUE_MASK2 = (
    np.array([0, 60, 60]),
    np.array([60, 255, 255]),
)

def initialize_rgb_camera(process):
    """
    Set up the RGB camera
    """
    # Create the camera object
    camera = Picamera2()

    # Set the process variable `rgb-cam`
    process.setvar("rgb-cam", camera)

    # Configure the camera
    camera_config = camera.create_still_configuration(
        main={"size": (640, 480)},
    )
    camera.configure(camera_config)

    # Start the camera
    camera.start()

def capture_rgb_image(process):
    """
    Capture an RGB image
    """
    # Get the camera
    camera = process.getvar("rgb-cam")

    # Capture a PIL-compatible image
    pil_image = camera.capture_image("main")

    # Convert the image color profile
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_BGR2HSV)

    # Create the image mask
    mask1 = cv2.inRange(image, *BLUE_MASK1)
    mask2 = cv2.inRange(image, *BLUE_MASK2)
    mask = mask1 + mask2

    # Apply the image mask
    masked_img = cv2.bitwise_and(image, image, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # If we have contours...
    if len(contours) != 0:
        # Find the biggest countour by area
        c = max(contours, key=cv2.contourArea)

        # Get a bounding rectangle around that contour
        x, y, w, h = cv2.boundingRect(c)

        # Draw the rectangle on our frame
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save the image file
    cv2.imwrite("test.jpg", image)

#######################################################################################
# The copyright to the code below is owned by Joshua Hrisko, Maker Portal LLC (2021). #
# The code has been modified slightly by Joseph Hobbs, CASCADE to fit the programming #
# conventions of this project.                                                        #
#######################################################################################

def initialize_ir_camera(process):
    """
    Set up the IR camera
    """
    t0 = time.time()
    sensor = []
    while (time.time() - t0) < 1: # wait 1sec for sensor to start
        try:
            # AD0 = GND, addr = 0x68 | AD0 = 5V, addr = 0x69
            sensor = amg8833_i2c.AMG8833(addr=0x69) # start AMG8833
        except:
            sensor = amg8833_i2c.AMG8833(addr=0x68)
        finally:
            pass
    time.sleep(0.1) # wait for sensor to settle

    # If no device is found, exit the script
    if not sensor:
        raise Exception("Could not find connected AMG8833")

def capture_ir_image(process):
    """
    Capture an IR image
    """
    pix_to_read = 64 # read all 64 pixels
    status, pixels = sensor.read_temp(pix_to_read) # read pixels with status
    if status: # if error in pixel, re-enter loop and try again
        continue
    print(f"Pixels:\n{pixels}")

    T_thermistor = sensor.read_thermistor() # read thermistor temp
    print(f"Thermistor Temperature: {round(T_thermistor, 2)}") # print thermistor temp