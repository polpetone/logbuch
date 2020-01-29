from typing import List

from src.portadapter.input.migration.domain.MetaTask import MetaTask


class Stat:

    def __init__(self, logFiles):
        self.logFiles = logFiles

    def get_task_count(self):
        task_count = 0
        for logFile in self.logFiles:
            task_count = task_count + len(logFile.tasks)
        return task_count

    def get_uniq_location_count(self):
        locations = set()
        for logFile in self.logFiles:
            locations.add(logFile.location)
        return len(locations)

    def get_location_date_dict(self):
        location_date_dict = dict()
        for logFile in self.logFiles:
            location_date_dict[logFile.date] = logFile.location
        return location_date_dict

    def generate_meta_tasks(self) -> List[MetaTask]:
        all_tasks = []

        meta_tasks = []

        for log_file in self.logFiles:
            all_tasks += log_file.tasks

        for task in all_tasks:
            meta_task = find_matching_meta_task(meta_tasks, task)
            if meta_task is not None:
                meta_task.append_task(task)
            else:
                new_meta_task = MetaTask(task)
                meta_tasks.append(new_meta_task)

        return meta_tasks


def find_matching_meta_task(meta_tasks, task):
    for meta_task in meta_tasks:
        if meta_task.initial_task.text == task.text:
            return meta_task
    return None


