#!/bin/python3
# CASCADE FSW
# Main executable

import time

# Import main process
from process import Process

def p1(process):
    process.block_until(-5)
    process.hold()

def p2(process):
    while process.until(0):
        print(f"{process.time}\r", end="")
    print()

if __name__ == "__main__":
    # Initialize the main process
    cascade = Process(countdown=10)

    # Queue tasks
    cascade.add(p1)
    cascade.add(p2)

    # Execute the main process
    cascade.run()