from datetime import datetime


class TaskView(object):

    def __init__(self, task, select_number):
        self.task = task
        self.select_number = select_number
        if task.date:
            self.date = datetime.fromisoformat(task.date).strftime("%d-%m-%Y %H:%M:%S")
        else:
            self.date = ""
        self.text = task.text
        self.shortened_text = task.text[:35]
        self.status = task.status.status
        if task.status.date:
            self.status_date = datetime.fromisoformat(task.status.date).strftime("%d-%m-%Y %H:%M:%S")
        else:
            self.status_date = ""
        self.sub_task_views = []
        sub_task_counter = 0
        for sub_task in task.sub_tasks:
            sub_task_counter += 1
            self.sub_task_views.append(TaskView(sub_task, sub_task_counter))

    def get_sub_task_view_by_number(self, number):
        result = [x for x in self.sub_task_views if x.select_number == number]
        if len(result) > 0:
            return result[0]
        return None

    def simple_view(self, with_header=False):
        template = "{0:<40}{1:<30}{2:<40}{3:<20}{4:<30}\n"
        sub_task_template = "{0:<30}{1:<40}{2:<30}{3:<40}{4:<20}{5:<30}\n"

        if with_header:
            out = template.format("uid", "Date", "Text", "Status", "Status Date")
            out += template.format(self.task.uid, self.date, self.shortened_text, self.status, self.status_date)
        else:
            out = template.format(self.task.uid, self.date, self.shortened_text, self.status, self.status_date)

        for sub_task_view in self.sub_task_views:
            out += sub_task_template.format("",
                                            sub_task_view.task.uid,
                                            sub_task_view.date,
                                            sub_task_view.shortened_text,
                                            sub_task_view.status,
                                            sub_task_view.status_date)

        return out
