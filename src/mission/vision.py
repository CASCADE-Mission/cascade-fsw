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
