# CASCADE FSW
# Main process

from logger import Logger
from task import Task
from timer import Timer

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

        # Initialize process timer
        self.timer = Timer()

        # Set countdown
        self.countdown = countdown

    @property
    def time(self):
        """
        Get process time
        """
        return self.timer.time - self.countdown

    def block(self, time):
        """
        Block this process by a specified amount of time
        """
        time.sleep(time)

    def block_until(self, until):
        """
        Block this process until a certain timer value
        """
        while self.time < until:
            pass

    def hold(self):
        """
        Perform a hold
        """
        self.timer.stop()
        input("Performing scheduled hold >> ")
        self.timer.start()

    def add(self, function, name=None, success=None, failure=None, priority=0):
        """
        Queue a task and sort the queue
        """
        # Construct a `Task` object
        task = Task(function, name, success, failure, priority)

        # Append the task to the queue
        self.queue.append(task)

        # Log the task
        self.log(f"{str(task)} queued")
        
        # Sort the queue
        self.queue.sort(reverse=True, key=by_priority)

    def log(self, message, priority=0):
        """
        Log a message to the process log
        """
        self.logger.log(message, priority)

    def execute(self, task):
        """
        Execute a task in a safe environment
        """
        # Log the task
        self.log(f"{str(task)} started")

        try:
            # Execute the task
            task(self)
            self.log(task.success)
        except Exception:
            self.log(task.failure, priority=task.priority)
        
        # Log the task
        self.log(f"{str(task)} finished")

    def run(self):
        """
        Run the main process
        """
        # Log the initialization
        self.log("Main process successfully initialized")

        # Start the timer
        self.timer.start()

        while self.queue:
            # Get the highest-priority task
            task = self.queue.pop(0)

            # Execute this task
            self.execute(task)

        # Stop the timer
        self.timer.stop()

        # Log completion
        self.log(f"Main process terminating, all tasks completed")
