# CASCADE FSW
# Mission tasks

# Import tasks
from mission.vision import initialize_rgb_camera, capture_rgb_image, initialize_ir_camera, capture_ir_image, fuse_images

# Define countdown here
COUNTDOWN = 10 # seconds

# Task queue
TASKS = {
    initialize_rgb_camera: 0,
    initialize_ir_camera: 0,
    capture_rgb_image: 0,
    capture_ir_image: 0,
    fuse_images: 0,
}
