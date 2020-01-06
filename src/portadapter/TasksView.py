from src.portadapter.TaskView import TaskView


class TasksView(object):

    def __init__(self, tasks):
        self.tasks = tasks

    def simple_table_view(self):
        template = "{0:<5}{1:<30}{2:<40}{3:<20}\n"
        gap_template = "{0:<100}\n"
        sub_task_template = "{0:<20}{1:<5}{2:<30}{3:<40}{4:<20}\n"
        out = template.format("Nr", "Date", "Text", "Status")
        select_number = 0
        for task in self.tasks:
            select_number += 1
            task_view = TaskView(task=task, select_number=select_number)
            out += gap_template.format("----------------------------------------------------------------------------------")
            out += template.format(task_view.select_number, task_view.date, task_view.text, task_view.status)
            out += "\n"
            sub_task_select_number = 0
            for sub_task in task.sub_tasks:
                sub_task_select_number += 1
                sub_task_view = TaskView(task=sub_task, select_number=sub_task_select_number)
                out += sub_task_template.format("", sub_task_view.select_number, sub_task_view.date, sub_task_view.text, sub_task_view.status)
            out += "\n"

        return out
