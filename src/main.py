#!/bin/python3
# CASCADE FSW
# Main executable

import time

# Import main process
from process import Process

def countdown():
    time.sleep(5)

def scheduled_hold_one():
    input("Performing scheduled hold >> ")

def countdown_continued():
    time.sleep(5)

if __name__ == "__main__":
    # Initialize the main process
    cascade = Process(countdown=10)

    cascade.add(countdown)
    cascade.add(scheduled_hold_one)
    cascade.add(countdown_continued)

    # Execute the main process
    cascade.run()