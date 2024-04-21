# CASCADE FSW

Workspace for CASCADE Flight Software development.

# FSW Task Management

CASCADE FSW automatically completes task management and prioritization.

## Task Function Definition

Schedule tasks by importing their associated functions to `src/queue.py`.

Task functions must have one argument (by default, this argument is named `process`).  This argument represents the main process.

Process attributes:
- `process.time`: Current program time.  Note that, if `COUNTDOWN` is not set to zero, then this will be seconds after *zero*, not seconds after *program start*.

Process methods:
- `process.block(time: float)`: Block *the current task* for a specified `time` (in seconds).
- `process.block_until(epoch: float)`: Block *the current task* until the program timer achieves a specified `epoch` (in seconds).  Note that, if `COUNTDOWN` is not set to zero, then this will be seconds after *zero*, not seconds after *program start*.
- `process.hold()`: Block *all tasks* and *pauses the program timer* and waits for user command to resume.
- `process.log(message: str, priority: int)`: Add a message to the process log, marking the message with a given `priority`.  See `Task Prioritization` (below) for priority values.
- `process.add(function, priority: int)`: Add a task `function` with a given `priority` to the queue.
- `process.setvar(name: str, variable)`: Add a process variable, accessible from other tasks.
- `process.getvar(name: str)`: Get a process variable or raise an exception if the variable does not exist.

## Task Prioritization

Add each task to the `TASKS` dictionary.  The key should be the task function name and the value should be its priority.

Task priorities:
- 3: Emergent
- 2: Urgent
- 1: Priority
- 0: Routine

## Program Execution

To execute the program, simply run the following.

```
$ python3 src/main.py
```

# Process Log

The process log is contained in `logs/cascade.log` by default.