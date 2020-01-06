from datetime import datetime


class TaskView(object):

    def __init__(self, task, select_number):
        self.task = task
        self.select_number = select_number
        self.date = datetime.fromisoformat(task.date).strftime("%d-%m-%Y %H:%M:%S")
        self.text = task.text
        self.status = task.status.status
        self.sub_tasks = []
        sub_task_counter = 0
        for sub_task in task.sub_tasks:
            sub_task_counter += 1
            self.sub_tasks.append(TaskView(sub_task, sub_task_counter))
