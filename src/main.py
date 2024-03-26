#!/bin/python3
# CASCADE FSW
# Main executable

import time

# Import main process
from process import Process

if __name__ == "__main__":
    # Initialize the main process
    cascade = Process(countdown=10)

    # Queue tasks
    pass

    # Execute the main process
    cascade.run()