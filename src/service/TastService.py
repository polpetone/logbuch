import jsonpickle

from src.domain.Task import Task
from src.portadapter.TasksView import TasksView
from src.service.Tasks import Tasks

task_repo_file_path = "data/task_repo_file.json"


class TaskService:

    def __init__(self):
        self.tasks = self.load_tasks()

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

    def filter_tasks_by_status(self, status):
        result = [x for x in self.tasks if x.status.status == status]
        return result

    ## broken architecture, service should not know view
    def get_tasks_view(self):
        return TasksView(self.tasks)
