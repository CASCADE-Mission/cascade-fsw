# CASCADE FSW
# Computer Vision

import time
import sys

import cv2
import numpy as np
from picamera2 import Picamera2
from scipy import interpolate

from mission import amg8833_i2c

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
    camera = cv2.VideoCapture(0)

    # Set the process variable `rgb-cam`
    process.setvar("rgb-cam", camera)

def capture_rgb_image(process):
    """
    Capture an RGB image
    """
    # Get the camera
    camera = process.getvar("rgb-cam")

    # Capture an image
    _, image = camera.read() 

    process.setvar("bgr-img", image)

def fuse_images(process):
    """
    Fuse a BGR image to an IR image
    """
    
    # Get BGR and IR images

    rgb_img = cv2.cvtColor(
        process.getvar("bgr-img"),
        cv2.COLOR_BGR2RGB,
    )

    ir_img = process.getvar("ir-img")

    # Crop BGR image

    xmin = int(rgb_img.shape[1] / 2 - rgb_img.shape[0] / 2)
    xmax = int(xmin + rgb_img.shape[0])
    ymin = 0
    ymax = rgb_img.shape[0]

    # Resize BGR image to 256x256 image

    rgb_img_unsized = rgb_img[ymin:ymax, xmin:xmax]
    rgb_img = cv2.resize(rgb_img_unsized, (256, 256), interpolation=cv2.INTER_LINEAR)

    # Invert IR image

    inverted_ir_img = (255 * (1 - ir_img/25)).astype(np.uint8)

    # Construct mask

    image = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(image, *BLUE_MASK1)
    mask2 = cv2.inRange(image, *BLUE_MASK2)
    mask = mask1 + mask2

    fused = (255 * (mask/255) * (inverted_ir_img/255)).astype(np.uint8)

    color_fused = cv2.cvtColor(fused, cv2.COLOR_GRAY2BGR)

    # contours, _ = cv2.findContours(fused, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # # If we have contours...
    # if len(contours) != 0:
    #     # Find the biggest countour by area
    #     c = max(contours, key = cv2.contourArea)

    #     # Get a bounding rectangle around that contour
    #     x,y,w,h = cv2.boundingRect(c)

    #     cv2.rectangle(color_fused,(x,y),(x+w,y+h),(0,255,0),2)

    # print(x + w/2, y + h/2)

    process.setvar("fused-img", color_fused)

    # TODO: remove this
    cv2.imwrite("fused.jpg", color_fused)

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

    # Save the camera as a process variable
    process.setvar("ir-cam", sensor)

def capture_ir_image(process):
    """
    Capture an IR image
    """
    # Get the camera
    sensor = process.getvar("ir-cam")

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

    # Save the image
    process.setvar("ir-img", img)

    # Read and save the thermistor temperature
    T_thermistor = sensor.read_thermistor()
    process.setvar("temp", T_thermistor)