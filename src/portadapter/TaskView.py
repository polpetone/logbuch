from datetime import datetime


class TaskView(object):

    def __init__(self, task):
        self.task = task
        self.date = datetime.fromisoformat(task.date).strftime("%d-%m-%Y %H:%M:%S")
        self.text = task.text
        self.status = task.status.status
