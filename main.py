from src.domain.Task import Task
from src.service.TastService import TaskService


def test0():
    task_service = TaskService()
    task0 = task_service.create_task("Some Task")
    task1 = task_service.create_task("Some Task2")
    task1.sub_tasks.append(Task("sub task for Task2"))
    task0.change_status(status="CLOSED")
    task_service.save_tasks()
    tasks = task_service.get_tasks()
    print(tasks)


def test1():
    task_service = TaskService()
    tasks = task_service.get_tasks()
    template = "{0:<30}{1:<40}{2:<20}\n"
    sub_task_template = "{0:<20}{1:<30}{2:<40}{3:<20}\n"
    out = template.format("Sub Task", "Date", "Text", "Status")
    for task in tasks:
        out += "-----------------------------------------------------\n"
        out += template.format(task.date, task.text, task.status.status)
        for sub_task in task.sub_tasks:
            out += sub_task_template.format("", sub_task.date, sub_task.text, sub_task.status.status)
    return out


if __name__ == "__main__":
    test0()
    out = test1()
    print(out)
