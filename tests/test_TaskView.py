from unittest import TestCase
from src.domain.Task import Task
from src.portadapter.out.TaskView import TaskView


def create_detail_view_string(task_view, text, task_date, status, status_date):
    id_line = "        uid: {}".format(task_view.task.uid)
    date_line = "       task_date: {}".format(task_date)
    text_line = "       text: {}".format(text)
    status_line = "     task_status: {}".format(status)
    status_date_line = "status_date: {}".format(status_date)

    out = id_line + "\n"
    out += date_line + "\n"
    out += text_line + "\n"
    out += status_line + "\n"
    out += status_date_line + "\n  \n"
    return out


class TestTaskView(TestCase):

    def test_alter_task(self):
        task = Task("foobar")
        task_view = TaskView(task, 0)
        out = create_detail_view_string(task_view,
                                        "altered foobar",
                                        "02-04-2020 18:53:47",
                                        "FINISHED",
                                        "03-04-2020 18:53:47")
        altered_task_view = task_view.parse_from_detail_view_string(out)

        assert altered_task_view.task.uid == task_view.task.uid
        assert altered_task_view.task.date.strftime("%d-%m-%Y %H:%M:%S") == "02-04-2020 18:53:47"
        assert altered_task_view.task.status.date.strftime("%d-%m-%Y %H:%M:%S") == "03-04-2020 18:53:47"
        assert altered_task_view.task.text == 'altered foobar'
        assert altered_task_view.task.status.status == "FINISHED"
