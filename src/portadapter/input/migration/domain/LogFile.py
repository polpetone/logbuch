from datetime import datetime
from typing import List

from src.portadapter.input.migration.domain import TaskStatus
from src.portadapter.input.migration.domain.Task import Task


class LogFile:

    def __init__(self, date: datetime, location, tasks: List[Task]):
        self.date: datetime = date
        self.location = location
        self.tasks: List[Task] = tasks

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        filtered_tasks = [task for task in self.tasks if task.status == status]
        return filtered_tasks
