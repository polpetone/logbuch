from datetime import datetime
import json

from src.domain.TaskStatus import TaskStatus


class Task:

    def __init__(self, text, status, uuid, date):
        self.text = text
        self.status = status
        self.uuid = uuid
        self.date = date

    def change_status(self, status):
        self.status = TaskStatus(status, datetime.now().isoformat())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
