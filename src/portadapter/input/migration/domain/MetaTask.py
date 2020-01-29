class MetaTask:
    def __init__(self, initial_task):
        self.initial_task = initial_task
        self.tasks = []

    def append_task(self, task):
        self.tasks.append(task)

    def get_status(self):
        if len(self.tasks) > 0:
            oldest_task = max(self.tasks, key=lambda x: x.date)
            return oldest_task.status
        return self.initial_task.status
