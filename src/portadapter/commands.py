import click

from src.domain.Task import Task
from src.service.TastService import TaskService

task_service = TaskService()


@click.group()
def logbuch():
    """Logbuch"""


def print_simple_task_list():
    print(task_service.get_tasks_view().simple_table_view())


@logbuch.command()
def tasks():
    print_simple_task_list()


@logbuch.command()
@click.option("--nr", type=click.IntRange(0, 20), prompt="nr", help="Select a task by number")
def task(nr):
    tasks_view = task_service.get_tasks_view()
    task_view = tasks_view.get_task_view_by_number(nr)
    if task_view:
        print(task_view.simple_view())


@logbuch.command()
@click.option("--text", prompt="Text", help="Text of the new Task")
def add_task(text):
    task_service.create_task(text)
    task_service.save_tasks()
    print_simple_task_list()


@logbuch.command()
@click.option("--nr", type=click.IntRange(0, 20), prompt="nr", help="Select a task by number")
@click.option("--text", prompt="Text", help="Text of the new Task")
def add_sub_task(nr, text):
    tasks_view = task_service.get_tasks_view()
    task_view = tasks_view.get_task_view_by_number(nr)
    if task_view:
        sub_task = Task(text)
        task_view.task.add_sub_task(sub_task)
        task_service.save_tasks()
        print_simple_task_list()
    else:
        click.echo("No Task found with number {}".format(nr))


@logbuch.command()
@click.option("--task-nr", type=click.IntRange(0, 20), prompt="task nr", help="Select a task by number")
@click.option("--sub-task-nr", type=click.IntRange(0, 20), prompt="sub task nr", help="Select a task by number")
@click.option("--status", prompt="status", help="OPEN, CANCELED, CLOSED")
def change_status(task_nr, sub_task_nr, status):
    tasks_view = task_service.get_tasks_view()
    task_view = tasks_view.get_task_view_by_number(task_nr)
    if task_view:
        sub_task_view = task_view.get_sub_task_view_by_number(sub_task_nr)
        if sub_task_view:
            sub_task_view.task.change_status(status)
            task_service.save_tasks()
        else:
            task_view.task.change_status(status)
            task_service.save_tasks()
    else:
        click.echo("No Task found with number {}".format(task_nr))



