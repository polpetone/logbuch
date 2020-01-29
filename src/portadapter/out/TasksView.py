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
        template = "{0:<40}{1:<30}{2:<40}{3:<20}{4:<30}\n"
        gap_template = "{0:<100}\n"
        out = template.format("Id", "Nr", "Date", "Text", "Status", "Status Date")
        for task_view in self.task_views:
            out += gap_template.format(
                "--------------------------------------------------------------------"
                "--------------------------------------------------------------------------------"
                "--------------------------------------------------------------------------------")

            out += task_view.simple_view()

        return out
