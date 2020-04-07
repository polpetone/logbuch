from datetime import datetime


class TaskView(object):

    def __init__(self, task, select_number):
        self.task = task
        self.select_number = select_number
        if task.date:
            self.date = task.date.strftime("%d-%m-%Y %H:%M:%S")
        else:
            self.date = ""
        self.text = task.text
        self.shortened_text = task.text[:55]
        self.status = task.status.status
        if task.status.date:
            self.status_date = task.status.date.strftime("%d-%m-%Y %H:%M:%S")
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

    def simple_view(self):
        template = "{0:<30}{1:<60}{2:<20}{3:<30}\n"
        sub_task_template = "{0:<30}{1:<30}{2:<60}{3:<20}{4:<30}\n"
        gap_template = "{0:<160}\n"

        out = template.format(self.date, self.shortened_text, self.status, self.status_date)

        if len(self.sub_task_views) > 0:
            out += gap_template.format(200 * ".")

        for sub_task_view in self.sub_task_views:
            out += sub_task_template.format("",
                                            sub_task_view.date,
                                            sub_task_view.shortened_text,
                                            sub_task_view.status,
                                            sub_task_view.status_date)

        return out

    def detail_view(self):

        id_line = "        uid: {}".format(self.task.uid)
        date_line = "       task_date: {}".format(self.date)
        text_line = "       text: {}".format(self.task.text)
        status_line = "     status: {}".format(self.status)
        status_date_line = "status_date: {}".format(self.status_date)

        out = id_line + "\n"
        out += date_line + "\n"
        out += text_line + "\n"
        out += status_line + "\n"
        out += status_date_line + "\n  \n"

        if len(self.sub_task_views) > 0:
            sub_task_out = "---- sub tasks ---- \n  \n"
        else:
            sub_task_out = ""

        for sub_task_view in self.sub_task_views:
            sub_task_out += sub_task_view.detail_view()

        return out + sub_task_out

    def parse_from_detail_view_string(self, detail_view_string):

        lines = detail_view_string.split("\n")
        for line in lines:
            if "text:" in line:
                text_line = line.split("text:")
                self.task.text = text_line[1].strip()
            if "task_date:" in line:
                text_line = line.split("task_date:")
                date_string = text_line[1].strip()
                self.task.date = datetime.strptime(date_string, "%d-%m-%Y %H:%M:%S")

        return TaskView(self.task, 0)
