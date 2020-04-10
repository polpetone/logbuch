import jsonpickle

from src.domain.Task import Task
from src.service.Tasks import Tasks
from src.portadapter.out.logger import init as init_logger
from src.conf import task_repo_file_path


class TaskService:

    def __init__(self):
        self.tasks = self.load_tasks()
        self.filtered_tasks = self.load_tasks()
        self.logger = init_logger(str(self.__class__.__module__))

    def create_task(self, text):
        task = Task(text)
        self.tasks.append(task)
        self.logger.debug("Task created uid {}".format(task.uid))
        return task

    def get_tasks(self):
        self.logger.debug("get_tasks -> {} tasks".format(len(self.tasks)))
        return self.tasks

    def save_tasks(self):
        with open(task_repo_file_path, 'w') as task_repo_file:
            task_repo_file.write(jsonpickle.encode(Tasks(self.tasks)))
        self.filtered_tasks = self.load_tasks()

    def load_tasks(self):
        with open(task_repo_file_path, 'r') as task_repo_file:
            tasks_json = task_repo_file.read()
        tasks = jsonpickle.decode(tasks_json).tasks
        return tasks

    def sort_filtered_tasks_by_status_date(self):
        self.filtered_tasks.sort(key=lambda x: x.status.date)

    def filter_tasks_by_status(self, status):
        self.filtered_tasks = [x for x in self.filtered_tasks if x.status.status == status]
        self.logger.debug("filter tasks by status: {} -> {} filtered tasks".format(status, len(self.filtered_tasks)))

    def filter_tasks_by_from_date(self, from_date):
        self.filtered_tasks = [x for x in self.filtered_tasks if x.date > from_date]
        self.logger.debug("filter tasks by date: {} -> {} filtered tasks".format(from_date, len(self.filtered_tasks)))

    def filter_tasks_by_from_status_date(self, from_date):
        self.filtered_tasks = [x for x in self.filtered_tasks if x.status.date > from_date]
        self.logger.debug("filter tasks by date: {} -> {} filtered tasks".format(from_date, len(self.filtered_tasks)))

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
        self.logger.debug("filter tasks by query: {} -> {} filtered tasks".format(query, len(self.filtered_tasks)))

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
            self.logger.debug("Deleted Task uid: {} Text: {}".format(found_task.uid, found_task.text))
        else:
            for task in self.tasks:
                result = [x for x in task.sub_tasks if x.uid == uid]
                if len(result) == 1:
                    found_task = result[0]
                    task.sub_tasks.remove(found_task)
                    self.save_tasks()
                    self.logger.debug("Deleted SubTask uid: {} Text: {}".format(found_task.uid, found_task.text))
                    break
        return found_task
