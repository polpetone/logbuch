from unittest import TestCase
from src.domain.Task import Task
from src.portadapter.out.TaskView import TaskView
from src.portadapter.out.TaskView import TASK_SEPARATOR


def create_detail_view_string(task_view, text, task_date, status, status_date):
    separator = TASK_SEPARATOR
    id_line = "        uid: {}".format(task_view.task.uid)
    date_line = "       task_date: {}".format(task_date)
    text_line = "       text: {}".format(text)
    status_line = "     task_status: {}".format(status)
    status_date_line = "status_date: {}".format(status_date)

    out = separator + "\n"
    out += id_line + "\n"
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
        task_view.parse_and_alter(out)

        assert task_view.task.uid == task_view.task.uid
        assert task_view.task.date.strftime("%d-%m-%Y %H:%M:%S") == "02-04-2020 18:53:47"
        assert task_view.task.status.date.strftime("%d-%m-%Y %H:%M:%S") == "03-04-2020 18:53:47"
        assert task_view.task.text == 'altered foobar'
        assert task_view.task.status.status == "FINISHED"

    def test_alter_task_with_sub_tasks(self):
        task = Task("foobar")
        sub_task_0 = Task("foobar sub 0")
        sub_task_1 = Task("foobar sub 1")
        task.sub_tasks = [sub_task_0, sub_task_1]
        task_view = TaskView(task, 0)

        out_task = create_detail_view_string(task_view,
                                             "altered foobar",
                                             "02-04-2020 18:53:47",
                                             "FINISHED",
                                             "03-04-2020 18:53:47")

        out_sub_0 = create_detail_view_string(task_view,
                                              "altered foobar sub 0",
                                              "02-04-2020 18:53:47",
                                              "FINISHED",
                                              "03-04-2020 18:53:47")

        out_sub_1 = create_detail_view_string(task_view,
                                              "altered foobar sub 1",
                                              "02-04-2020 18:53:47",
                                              "FINISHED",
                                              "03-04-2020 18:53:47")

        out = out_task + "\n" + out_sub_0 + "\n" + out_sub_1

        print(out)

        task_view.parse_and_alter(out)

        assert task_view.task.date.strftime("%d-%m-%Y %H:%M:%S") == "02-04-2020 18:53:47"
        assert task_view.task.status.date.strftime("%d-%m-%Y %H:%M:%S") == "03-04-2020 18:53:47"
        assert task_view.task.text == 'altered foobar'
        assert task_view.task.status.status == "FINISHED"

        assert task_view.task.sub_tasks[0].date.strftime("%d-%m-%Y %H:%M:%S") == "02-04-2020 18:53:47"
        assert task_view.task.sub_tasks[0].status.date.strftime("%d-%m-%Y %H:%M:%S") == "03-04-2020 18:53:47"
        assert task_view.task.sub_tasks[0].text == 'altered foobar sub 0'
        assert task_view.task.sub_tasks[0].status.status == "FINISHED"

        assert task_view.task.sub_tasks[1].date.strftime("%d-%m-%Y %H:%M:%S") == "02-04-2020 18:53:47"
        assert task_view.task.sub_tasks[1].status.date.strftime("%d-%m-%Y %H:%M:%S") == "03-04-2020 18:53:47"
        assert task_view.task.sub_tasks[1].text == 'altered foobar sub 1'
        assert task_view.task.sub_tasks[1].status.status == "FINISHED"
