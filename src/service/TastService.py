import uuid
from datetime import datetime
import json

from src.domain.Task import Task
from src.domain.TaskStatus import TaskStatus
from src.service.Tasks import Tasks

task_repo_file_path = "data/task_repo_file.json"


class TaskService:

    def __init__(self):
        self.tasks = self.load_tasks()
        #self.tasks = []

    def create_task(self, text):
        task = Task(text, TaskStatus("OPEN", datetime.now().isoformat()), str(uuid.uuid4()), datetime.now().isoformat())
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def save_tasks(self):
        with open(task_repo_file_path, 'w') as task_repo_file:
            task_repo_file.write(Tasks(self.tasks).to_json())

    def load_tasks(self):
        with open(task_repo_file_path, 'r') as task_repo_file:
            tasks_json = task_repo_file.read()
        t = json.loads(tasks_json)
        tasks_object = Tasks(**t)
        tasks = []
        for tasks_object in tasks_object.tasks:
            task = Task(**tasks_object)
            tasks.append(task)
        return tasks
