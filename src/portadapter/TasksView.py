from src.portadapter.TaskView import TaskView


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
        template = "{0:<40}{1:<5}{2:<30}{3:<40}{4:<20}{5:<30}\n"
        gap_template = "{0:<100}\n"
        sub_task_template = "{0:<30}{1:<40}{2:<5}{3:<30}{4:<40}{5:<20}{6:<30}\n"
        out = template.format("Id", "Nr", "Date", "Text", "Status", "Status Date")
        select_number = 0
        for task_view in self.task_views:
            select_number += 1
            out += gap_template.format(
                "--------------------------------------------------------------------"
                "--------------------------------------------------------------------------------"
                "--------------------------------------------------------------------------------")
            out += template.format(
                                   task_view.task.uid,
                                   task_view.select_number,
                                   task_view.date,
                                   task_view.text,
                                   task_view.status,
                                   task_view.status_date)
            sub_task_select_number = 0
            for sub_task_view in task_view.sub_tasks:
                sub_task_select_number += 1
                out += sub_task_template.format("",
                                                sub_task_view.task.uid,
                                                sub_task_view.select_number,
                                                sub_task_view.date,
                                                sub_task_view.text,
                                                sub_task_view.status,
                                                sub_task_view.status_date)

        return out
