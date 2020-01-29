from enum import Enum


class TaskStatus(Enum):
    OPEN = 1
    FINISHED = 2
    MOVED = 3
    CANCELED = 4


def task_status_to_string(status):
    if status == TaskStatus.OPEN:
        return "OPEN"
    if status == TaskStatus.FINISHED:
        return "FINISHED"
    if status == TaskStatus.CANCELED:
        return "CANCELED"
    if status == TaskStatus.MOVED:
        return "MOVED"
