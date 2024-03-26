# CASCADE FSW
# Data logger

from datetime import datetime

# Define a log message for CASCADE
class LogMessage:
    def __init__(self, msg, priority=0):
        """
        Create a log message

        Priority levels:
            3: Fatal
            2: Urgent
            1: Priority
            0: Routine (default)
        """
        # Get the current date & time
        self.datetime = datetime.now()

        # Set the message
        self.message = msg

        # Set the priority
        self.priority = priority
    
    def __str__(self):
        """
        Convert this log message to a string
        """
        # Set priority
        priority = None
        match self.priority:
            case 0:
                priority = "ROUTINE"
            case 1:
                priority = "PRIORITY"
            case 2:
                priority = "URGENT"
            case 3:
                priority = "FATAL"
            case _:
                priority = "UNKNOWN"

        # Make human-readable datetime
        datetime = f"{self.datetime.year:0>4}-{self.datetime.month:0>2}-{self.datetime.day:0>2} {self.datetime.hour:0>2}:{self.datetime.minute:0>2}:{self.datetime.second:0>2}.{self.datetime.microsecond:0>6}"

        return f"[{datetime}] [{priority}] {self.message}\n"

# Define a logger for CASCADE
class Logger:
    def __init__(self, logfile="cascade.log"):
        """
        Create a logger
        """
        # Set the log file
        self.file = "logs/" + logfile

    def log(self, msg, priority=0):
        """
        Log this message to the specified file
        """
        # Construct log message
        message = LogMessage(msg, priority)

        # Write log message
        with open(self.file, "a") as f:
            f.write(str(message))