import click

from src.portadapter.TasksView import TasksView
from src.service.TastService import TaskService

task_service = TaskService()


@click.group()
def logbuch():
    """Logbuch"""


@logbuch.command()
def tasks():
    task_list = task_service.get_tasks()
    task_view = TasksView(task_list)
    print(task_view.simple_table_view())
