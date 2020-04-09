from src.portadapter.out.TaskView import TaskView


class TasksView(object):

    def __init__(self, tasks):
        self.task_views = []
        task_counter = 0
        for task in tasks:
            task_counter += 1
            self.task_views.append(TaskView(task, task_counter))

    def simple_table_view(self):
        template = "{0:<30}{1:<60}{2:<20}{3:<30}\n"
        gap_template = "{0:<160}\n"
        out = template.format("Date", "Text", "Status", "Status Date")
        for task_view in self.task_views:
            out += gap_template.format(200 * "-")
            out += task_view.view_with_notes()
            out += "\n"
        return out

    def simple_table_view_with_uid(self):
        template = "{0:<50}{1:<30}{2:<60}{3:<20}{4:<30}\n"
        gap_template = "{0:<160}\n"
        out = template.format("ID", "Date", "Text", "Status", "Status Date")
        for task_view in self.task_views:
            out += gap_template.format(200 * "-")
            out += task_view.simple_view_with_uid()
            out += "\n"
        return out
