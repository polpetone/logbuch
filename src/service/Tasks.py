import json


class Tasks:

    def __init__(self, tasks):
        self.tasks = tasks

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
