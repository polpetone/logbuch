import click

from src.domain.Task import Task
from src.domain.TaskStatus import TaskStatus
from src.portadapter.input.migration.domain.LogFileService import LogFileService
from src.portadapter.input.migration.domain.TaskStatus import task_status_to_string
from src.portadapter.input.migration.log_file_parser import LogFileParser
from src.portadapter.out.TaskView import TaskView
from src.portadapter.out.TasksView import TasksView
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
        click.echo("No Task found with number {}".format(uid))


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


@logbuch.command()
def migration():
    path = "/home/icke/.logbuch/"
    log_file_parser = LogFileParser()
    log_file_service = LogFileService(log_file_parser)
    log_files = log_file_service.get_log_files(path)
    counter = 0
    for log_file in log_files:
        task_count = len(log_file.tasks)
        counter += task_count
        for task in log_file.tasks:
            migrated_task = Task(
                text=task.text,
                status=TaskStatus(task_status_to_string(task.status)),
                uid=str(task.uuid),
                date=task.date.isoformat(),
            )

            for sub_task in task.sub_tasks:
                date = None
                if sub_task.date:
                    date = sub_task.date.isoformat()

                migrated_sub_task = Task(
                    text=sub_task.text,
                    status=TaskStatus(task_status_to_string(sub_task.status)),
                    uid=str(sub_task.uuid),
                    date=date
                )
                migrated_task.sub_tasks.append(migrated_sub_task)

            insert_and_delete_duplicate(task_service.tasks, migrated_task)

    task_service.save_tasks()
    click.echo("{} Tasks loaded for migration".format(counter))
    click.echo("{} Tasks".format(len(task_service.tasks)))


def insert_and_delete_duplicate(tasks, task):
    result = [x for x in tasks if x.text == task.text]
    if len(result) == 1:
        deleted_task = task_service.delete_task_by_id(result[0].uid)
        if deleted_task is not None:
            print("Deleted Task {}".format(deleted_task.uid))
    tasks.append(task)
