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
    template = "{0:<30}{1:<40}\n"
    out = template.format("Date", "Text")
    for task in tasks:
        out += template.format(task.date, task.text)
    return out


if __name__ == "__main__":
    out = test1()
    print(out)
