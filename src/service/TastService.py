import json

import jsonpickle

from src.domain.Task import Task
from src.service.Tasks import Tasks

task_repo_file_path = "data/task_repo_file.json"


class TaskService:

    def __init__(self):
        self.tasks = self.load_tasks()
        #self.tasks = []

    def create_task(self, text):
        task = Task(text)
        self.tasks.append(task)
        return task

    def get_tasks(self):
        return self.tasks

    def save_tasks(self):
        with open(task_repo_file_path, 'w') as task_repo_file:
            task_repo_file.write(jsonpickle.encode(Tasks(self.tasks)))

    def load_tasks(self):
        with open(task_repo_file_path, 'r') as task_repo_file:
            tasks_json = task_repo_file.read()
        tasks = jsonpickle.decode(tasks_json).tasks
        return tasks