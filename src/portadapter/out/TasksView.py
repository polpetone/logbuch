from src.portadapter.out.TaskView import TaskView


class TasksView(object):

    def __init__(self, tasks):
        self.task_views = []
        for task in tasks:
            self.task_views.append(TaskView(task))

    def simple_table_view(self, gab_char=""):
        template = "{0:<30}{1:<80}{2:<10}{3:<30}\n"
        gap_template = "{0:<160}\n"
        out = template.format("Date", "Text", "Status", "Status Date")
        for task_view in self.task_views:
            out += gap_template.format(180 * gab_char)
            out += task_view.view_with_notes()
            out += "\n"
        return out

    def simple_table_view_with_uid(self, gab_char=""):
        template = "{0:<50}{1:<30}{2:<80}{3:<10}{4:<30}\n"
        gap_template = "{0:<160}\n"
        out = template.format("ID", "Date", "Text", "Status", "Status Date")
        for task_view in self.task_views:
            out += gap_template.format(180 * gab_char)
            out += task_view.simple_view_with_uid()
            out += "\n"
        return out
