# CASCADE FSW
# Main process

from logger import Logger
from task import Task

def by_priority(task):
    """
    Sorting key for tasks
    """
    return task.priority

class Process:
    def __init__(self, logger=None):
        """
        Create a new process
        """
        # Initialize logger
        if logger is None:
            logger = Logger()
        self.logger = logger

        # Initialize task queue
        self.queue = []

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
            task.run()
            self.logger.log(task.success)
        except Exception:
            self.logger.log(task.failure, priority=task.priority)
        
        # Log the task
        self.logger.log(f"{str(task)} finished")

    def run(self):
        """
        Run the main process
        """
        # Log the initialization
        self.logger.log("Main process successfully initialized")

        while self.queue:
            # Get the highest-priority task
            task = self.queue.pop(0)

            # Execute this task
            task()

        # Log completion
        self.logger.log(f"Main process terminating, all tasks completed")
