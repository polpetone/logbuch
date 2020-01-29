from enum import Enum


class TaskStatus(Enum):
    OPEN = 1
    FINISHED = 2
    MOVED = 3
    CANCELED = 4
