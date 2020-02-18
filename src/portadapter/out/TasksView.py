from src.portadapter.out.TaskView import TaskView


class TasksView(object):

    def __init__(self, tasks):
        self.task_views = []
        task_counter = 0
        for task in tasks:
            task_counter += 1
            self.task_views.append(TaskView(task, task_counter))

    def get_task_view_by_number(self, number):
        result = [x for x in self.task_views if x.select_number == number]
        if len(result) > 0:
            return result[0]
        return None

    def simple_table_view(self):
        template = "{0:<30}{1:<40}{2:<20}{3:<30}\n"
        gap_template = "{0:<160}\n"
        out = template.format("Date", "Text", "Status", "Status Date")
        for task_view in self.task_views:
            out += gap_template.format(200 * "-")
            out += task_view.simple_view()
            out += "\n"

        return out
