import json
from datetime import datetime


class TaskStatus(object):

    def __init__(self, status="OPEN", date=datetime.now()):
        self.status = status
        self.date = date

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

