from datetime import datetime
import uuid
import json
from src.portadapter.input.migration.domain.TaskStatus import TaskStatus


class Task:

    def __init__(self, status=TaskStatus.OPEN, text=""):
        self.text = text
        self.uuid = uuid.uuid4()
        self.status = status
        self.sub_tasks = []
        self.additions = []
        self.date = None

    def change_status(self, task_status: TaskStatus):
        self.status = task_status

    def append_sub_task(self, task):
        self.sub_tasks.append(task)

    def append_addition(self, addition: str):
        self.additions.append(addition)

    def count_open_sub_tasks(self):
        count = 0
        for task in self.sub_tasks:
            if TaskStatus.OPEN == task.status:
                count = count + 1
        return count

    def set_date(self, date: datetime):
        self.date = date

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_string(self):
        return self.text
