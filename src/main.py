#!/bin/python3
# CASCADE FSW
# Main executable

import time

# Import main process
from process import Process

# Import tasks
from tasklist import COUNTDOWN, TASKS

if __name__ == "__main__":
    # Initialize the main process
    cascade = Process(countdown=COUNTDOWN)

    # Queue tasks
    for task, priority in TASKS.items():
        cascade.add(task, priority=priority)

    # Execute the main process
    cascade.run()
