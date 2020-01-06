import uuid
from datetime import datetime
import json
from src.domain.TaskStatus import TaskStatus


class Task(object):

    def __init__(self,
                 text,
                 status=TaskStatus(),
                 uid=str(uuid.uuid4()),
                 date=datetime.now().isoformat(),
                 sub_tasks=None):
        if sub_tasks is None:
            sub_tasks = list()
        self.text = text
        self.status = status
        self.uid = uid
        self.date = date
        self.sub_tasks = sub_tasks

    def add_sub_task(self, task):
        self.sub_tasks.append(task)

    def change_status(self, status):
        self.status = TaskStatus(status, datetime.now().isoformat())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
