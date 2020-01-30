import jsonpickle

from src.domain.Task import Task
from src.service.Tasks import Tasks

task_repo_file_path = "data/m.json"


class TaskService:

    def __init__(self):
        self.tasks = self.load_tasks()
        self.filtered_tasks = self.load_tasks()

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
        self.filtered_tasks = [x for x in self.filtered_tasks if x.status.status == status]

    def filter_tasks_by_from_date(self, from_date):
        self.filtered_tasks = [x for x in self.filtered_tasks if x.date > from_date]

    def get_task_by_id(self, uid):
        found_task = None
        result = [x for x in self.tasks if x.uid == uid]
        if len(result) == 1:
            found_task = result[0]
        else:
            for task in self.tasks:
                result = [x for x in task.sub_tasks if x.uid == uid]
                if len(result) == 1:
                    found_task = result[0]
                    break
        return found_task

    def delete_task_by_id(self, uid):
        found_task = None
        result = [x for x in self.tasks if x.uid == uid]
        if len(result) == 1:
            found_task = result[0]
            self.tasks.remove(found_task)
            self.save_tasks()
        else:
            for task in self.tasks:
                result = [x for x in task.sub_tasks if x.uid == uid]
                if len(result) == 1:
                    found_task = result[0]
                    task.sub_tasks.remove(found_task)
                    self.save_tasks()
                    break
        return found_task

    def filter_tasks_by_text_query(self, query):
        result = []
        for task in self.filtered_tasks:
            if query in task.text:
                result.append(task)
            else:
                for sub_task in task.sub_tasks:
                    if query in sub_task.text:
                        result.append(task)
                        break
        self.filtered_tasks = result
