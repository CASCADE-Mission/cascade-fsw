# CASCADE FSW
# Main process

import threading
import time

from logger import Logger
from task import Task

def by_priority(task):
    """
    Sorting key for tasks
    """
    return task.priority

class Process:
    def __init__(self, countdown=0, logger=None):
        """
        Create the main process
        """
        # Initialize logger
        if logger is None:
            logger = Logger()
        self.logger = logger

        # Initialize task queue
        self.queue = []

        # Initialize process time
        self.start = None

        # Set countdown
        self.countdown = countdown

    def time(self):
        """
        Get process time
        """
        if self.start is not None:
            return time.time() - self.start - self.countdown
        else:
            return None

    def add(self, function, name=None, success=None, failure=None, priority=0):
        """
        Queue a task and sort the queue
        """
        # Construct a `Task` object
        task = Task(function, name, success, failure, priority)

        # Append the task to the queue
        self.queue.append(task)

        # Log the task
        self.logger.log(f"{str(task)} queued")
        
        # Sort the queue
        self.queue.sort(reverse=True, key=by_priority)

    def execute(self, task):
        """
        Execute a task in a safe environment
        """
        # Log the task
        self.logger.log(f"{str(task)} started")

        try:
            # Execute the task
            task()
            self.logger.log(task.success)
        except Exception:
            self.logger.log(task.failure, priority=task.priority)
        
        # Log the task
        self.logger.log(f"{str(task)} finished")

    def run(self):
        """
        Run the main process
        """
        # Set process time
        self.start = time.time()

        # Log the initialization
        self.logger.log("Main process successfully initialized")

        while self.queue:
            # Get the highest-priority task
            task = self.queue.pop(0)

            # Execute this task
            self.execute(task)

        # Log completion
        self.logger.log(f"Main process terminating, all tasks completed")
