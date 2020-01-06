import click

from src.portadapter.TasksView import TasksView
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
@click.option("--nr", type=click.IntRange(0, 10), prompt="nr", help="Select a task by number")
def task(nr):
    click.echo("Selected {}".format(nr))


@logbuch.command()
@click.option("--text", prompt="Text", help="Text of the new Task")
def add_task(text):
    task_service.create_task(text)
    task_service.save_tasks()
    print_simple_task_list()
