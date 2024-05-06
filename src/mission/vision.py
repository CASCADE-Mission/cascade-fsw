# CASCADE FSW
# Computer Vision

import time

from picamera2 import Picamera2
import cv2
import numpy as np
from scipy import interpolate

from mission import amg8833_i2c

BLUE_MASK = (
    np.array([80, 40, 40]),
    np.array([160, 255, 255]),
)

def initialize_rgb_camera():
    """
    Set up the RGB camera
    """
    # Create the camera object
    camera = Picamera2()

    # Configure the camera object
    config = camera.create_still_configuration(main={"size": (256, 256)})
    camera.configure(config)

    # Start the camera
    camera.start()

    return camera

def capture_rgb_image(camera):
    """
    Capture an RGB image
    """
    # Capture an image
    image = camera.capture_array()

    # Convert to BGR color profile
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return image

def fuse_images(rgb_img, ir_img, min_feature_size):
    """
    Fuse an RGB image to an IR image

    Arguments:
        - `rgb_img`: a 256x256 NumPy array representing the RGB image
        - `ir_img`: a 256x256 NumPy array representing the IR image
    """
    image = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(image, *BLUE_MASK)

    fused = (255 * (mask/255) * (ir_img/255)).astype(np.uint8)

    color_fused = cv2.cvtColor(fused, cv2.COLOR_GRAY2BGR)

    contours, _ = cv2.findContours(fused, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    d = None

    # If we have contours...
    if len(contours) != 0:
        # Find the biggest countour by area
        c = max(contours, key = cv2.contourArea)

        # Get a bounding rectangle around that contour
        x,y,w,h = cv2.boundingRect(c)

        cv2.rectangle(color_fused,(x,y),(x+w,y+h),(0,255,0),2)

        # Determine characteristic dimension
        d = np.sqrt(w*w + h*h)

        if d > min_feature_size:
            print(f"Location: ({x + w/2}, {y + h/2}) | Size: {d}")

    return d

#######################################################################################
# The copyright to the code below is owned by Joshua Hrisko, Maker Portal LLC (2021). #
# The code has been modified slightly by Joseph Hobbs, CASCADE to fit the programming #
# conventions of this project.                                                        #
#######################################################################################

def initialize_ir_camera():
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

    return sensor

def capture_ir_image(sensor, k, t):
    """
    Capture an IR image
    """
    pix_to_read = 64 # read all 64 pixels
    status, pixels = sensor.read_temp(pix_to_read) # read pixels with status
    if status: # if error in pixel, re-enter loop and try again
        capture_ir_image(process)

    # original resolution
    pix_res = (8, 8) # pixel resolution
    xx, yy = (np.linspace(0, pix_res[0], pix_res[0]), np.linspace(0, pix_res[1], pix_res[1]))
    zz = np.zeros(pix_res) # set array with zeros first

    # new resolution
    pix_mult = 32 # multiplier for interpolation
    interp_res = (int(pix_mult * pix_res[0]), int(pix_mult * pix_res[1]))
    grid_x, grid_y = (np.linspace(0, pix_res[0], interp_res[0]), np.linspace(0, pix_res[1], interp_res[1]))

    def interp(z_var):
        """
        Using cubic interpolation, increase the resolution of the IR image
        """
        f = interpolate.interp2d(xx, yy, z_var, kind="cubic")
        return f(grid_x, grid_y)

    img = interp(np.reshape(pixels,pix_res))

    # Invert IR image
    img = (255 / (1 + np.exp(k * (img - t)))).astype(np.uint8)

    return img
