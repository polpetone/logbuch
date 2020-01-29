import click

from src.domain.Task import Task
from src.portadapter.TaskView import TaskView
from src.portadapter.TasksView import TasksView
from src.service.TastService import TaskService

task_service = TaskService()


@click.group()
def logbuch():
    """Logbuch"""


@logbuch.command()
@click.option("--status", help="OPEN, CANCELED, CLOSED")
def tasks(status):
    if status:
        tasks = task_service.filter_tasks_by_status(status)
    else:
        tasks = task_service.get_tasks()
    tasks_view = TasksView(tasks)
    click.echo(tasks_view.simple_table_view())


@logbuch.command()
@click.option("--uid", prompt="task id", help="Task id to get view for")
def task(uid):
    task = task_service.get_task_by_id(uid)
    if task:
        task_view = TaskView(task, None)
        click.echo(task_view.simple_view())
    else:
        click.echo("No Task found with uid {}".format(uid))

@logbuch.command()
@click.option("--uid", prompt="task id", help="Task id for task to get deleted")
def delete_task(uid):
    task = task_service.delete_task_by_id(uid)
    if task:
        click.echo("Task {} deleted".format(task.uid))
    else:
        click.echo("No Task found with uid {}".format(uid))

@logbuch.command()
@click.option("--text", prompt="Text", help="Text of the new Task")
def add_task(text):
    task_service.create_task(text)
    task_service.save_tasks()
    tasks = task_service.get_tasks()
    tasks_view = TasksView(tasks)
    click.echo(tasks_view.simple_table_view())


@logbuch.command()
@click.option("--uid", prompt="task id", help="Task id to add sub task for")
@click.option("--text", prompt="Text", help="Text of the new sub task")
def add_sub_task(uid, text):
    task = task_service.get_task_by_id(uid)
    if task:
        sub_task = Task(text)
        task.add_sub_task(sub_task)
        task_service.save_tasks()
        click.echo("Sub Task added for {}".format(uid))
    else:
        click.echo("No Task found with number {}".format(nr))


@logbuch.command()
@click.option("--uid", prompt="task id", help="Task id to change status for")
@click.option("--status", prompt="status", help="OPEN, CANCELED, CLOSED")
def change_status(uid, status):
    task = task_service.get_task_by_id(uid)
    if task:
        task.change_status(status)
        task_service.save_tasks()
    else:
        click.echo("No Task found with uid {}".format(uid))
