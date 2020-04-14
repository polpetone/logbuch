import uuid
from datetime import datetime
import json
from logbuch.domain.TaskStatus import TaskStatus
from logbuch.portadapter.out.logger import init as init_logger

# TODO: get file name automatic
logger = init_logger("logbuch.domain.Task")


class Task(object):

    def __init__(self,
                 text,
                 status=TaskStatus(),
                 uid=str(uuid.uuid4()),
                 date=datetime.now(),
                 sub_tasks=None):
        if sub_tasks is None:
            sub_tasks = list()
        self.text = text
        self.status = status
        self.uid = uid
        self.date = date
        self.notes = []
        self.sub_tasks = sub_tasks

    def add_sub_task(self, task):
        self.sub_tasks.append(task)

    def change_status(self, status):
        logger.debug("Changed Status from {} to {} for Task {}".format(self.status.status, status, self.uid))
        self.status = TaskStatus(status, datetime.now())

    def add_note(self, note):
        self.notes.append(note)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
