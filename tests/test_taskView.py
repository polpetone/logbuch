from unittest import TestCase
from src.domain.Task import Task
from src.portadapter.out.TaskView import TaskView


def create_detail_view_string(task_view, text):

    id_line = "        uid: {}".format(task_view.task.uid)
    date_line = "       date: {}".format(task_view.date)
    text_line = "       text: {}".format(text)
    status_line = "     status: {}".format(task_view.status)
    status_date_line = "status date: {}".format(task_view.status_date)

    out = id_line + "\n"
    out += date_line + "\n"
    out += text_line + "\n"
    out += status_line + "\n"
    out += status_date_line + "\n  \n"
    return out


class TestTaskView(TestCase):

    task = Task("foobar")
    task_view = TaskView(task, 0)
    out = create_detail_view_string(task_view, "altered text")
    altered_task_view = task_view.parse_from_detail_view_string(out)

    assert altered_task_view.task.uid == task_view.task.uid
    assert altered_task_view.task.text == "altered text"
