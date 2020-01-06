from src.portadapter.TaskView import TaskView


class TasksView(object):

    def __init__(self, tasks):
        self.tasks = tasks

    def simple_table_view(self):
        template = "{0:<30}{1:<40}{2:<20}\n"
        gap_template = "{0:<100}\n"
        sub_task_template = "{0:<20}{1:<30}{2:<40}{3:<20}\n"
        out = template.format("Date", "Text", "Status")
        for task in self.tasks:
            task_view = TaskView(task)
            out += gap_template.format("----------------------------------------------------------------------------------")
            out += template.format(task_view.date, task_view.text, task_view.status)
            out += "\n"
            for sub_task in task.sub_tasks:
                sub_task_view = TaskView(sub_task)
                out += sub_task_template.format("", sub_task_view.date, sub_task_view.text, sub_task_view.status)
            out += "\n"

        return out
