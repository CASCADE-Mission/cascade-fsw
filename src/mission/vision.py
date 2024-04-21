# CASCADE FSW
# Computer Vision

import cv2
import numpy
from picamera2 import Picamera2

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

    # Convert to OpenCV image
    image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2HSV)