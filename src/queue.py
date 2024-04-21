# CASCADE FSW
# Mission tasks

# Import tasks
from mission.vision import initialize_rgb_camera, capture_rgb_image

# Define countdown here
COUNTDOWN = 10 # seconds

# Define tasks here

# Task queue
TASKS = {
    initialize_rgb_camera: 0,
}