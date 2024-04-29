# CASCADE FSW
# Computer Vision

import cv2
import numpy as np
from picamera2 import Picamera2

BLUE_MASK = (
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
    mask1 = cv2.inRange(image, *BLUE_MASK)
    mask2 = cv2.inRange(image, *BLUE_MASK2)
    mask = mask1 + mask2

    # Apply the image mask
    masked_img = cv2.bitwise_and(image, image, mask=mask)

    # Save the image file
    cv2.imwrite("test.jpg", masked_img)
