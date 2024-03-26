# CASCADE FSW
# Mission tasks

class Task:
    def __init__(self, func, name=None, success=None, failure=None, priority=0):
        """
        Create a new task
        """
        # Set the task name
        if name is None:
            name = str(func)
        self.name = name

        # Set the task function
        self.function = func

        # Set the task priority
        self.priority = priority

        # Set the success message
        if success is None:
            success = f"{str(self.function)} succeeded"
        self.success = success

        # Set the failure message
        if failure is None:
            failure = f"{str(self.function)} failed"
        self.failure = failure
    
    def __str__(self):
        return self.name

    def __call__(self, process):
        self.function(process)