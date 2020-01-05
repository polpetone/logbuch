import json
from enum import Enum


class TaskStatus:

    def __init__(self, status, date):
        self.status = status
        self.date = date

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Status(Enum):
    CREATED = 1
    STARTED = 2
    BLOCKED = 3
    FINISHED = 4
    MOVED = 5
    CANCELED = 6
