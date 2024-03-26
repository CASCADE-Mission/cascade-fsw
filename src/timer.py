# CASCADE FSW
# Timer object

import time

class Timer:
    def __init__(self):
        """
        Create a new timer object
        """        
        # Elapsed time since last start
        self.elapsed = 0
        
        # Time accumulated
        self.accumulated = 0

        # Is the timer running?
        self.running = False

        # Time at last start
        self.started_time = None

        # Epoch at last start
        self.started_epoch = None

    def start(self):
        """
        Start this timer
        """
        self.started_time = self.time
        self.started_epoch = time.time()
        self.running = True

    def stop(self):
        """
        Stop this timer
        """
        if self.started_time is not None:
            self.accumulated += self.time - self.started_time
        self.running = False

    @property
    def time(self):
        """
        Get the time on this timer
        """
        if self.running:
            return time.time() - self.started_epoch + self.accumulated
        else:
            return self.accumulated