from src.domain.Task import Task
from src.portadapter.out.commands import logbuch
from src.service.TaskService import TaskService


def test0():
    task_service = TaskService()
    task0 = task_service.create_task("Some Task")
    task1 = task_service.create_task("Some Task2")
    task1.sub_tasks.append(Task("sub task for Task2"))
    task0.change_status(status="CLOSED")
    task_service.save_tasks()
    tasks = task_service.get_tasks()
    print(tasks)


if __name__ == "__main__":
    logbuch(prog_name='logbuch')
