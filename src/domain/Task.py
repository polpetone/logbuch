import uuid
from datetime import datetime
import json

from src.domain.TaskStatus import TaskStatus


class Task:

    def __init__(self,
                 text,
                 status=TaskStatus(),
                 uid=str(uuid.uuid4()),
                 date=datetime.now().isoformat()):
        self.text = text
        self.status = status
        self.uid = uid
        self.date = date

    def change_status(self, status):
        self.status = TaskStatus(status, datetime.now().isoformat())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
