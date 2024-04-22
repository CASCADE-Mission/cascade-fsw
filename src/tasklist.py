# CASCADE FSW
# Mission tasks

# Import tasks
from mission.vision import initialize_rgb_camera, capture_rgb_image

# Define countdown here
COUNTDOWN = 10 # seconds

# Task queue
TASKS = {
    initialize_rgb_camera: 0,
    capture_rgb_image: 0,
}
