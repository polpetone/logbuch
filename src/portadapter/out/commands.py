from datetime import datetime

import click

from src.domain.Task import Task
from src.domain.TaskStatus import TaskStatus
from src.portadapter.input.migration.domain.LogFileService import LogFileService
from src.portadapter.input.migration.domain.TaskStatus import task_status_to_string
from src.portadapter.input.migration.log_file_parser import LogFileParser
from src.portadapter.out.TaskView import TaskView
from src.portadapter.out.TasksView import TasksView
from src.portadapter.out.logger import init as init_logger
from src.service.TaskService import TaskService
from src.conf import logbuch_path

logger = init_logger("src.portadapter.out.commands")
task_service = TaskService()


@click.group()
def cli():
    """Logbuch"""


def get_open_tasks(ctx, args, incomplete):
    task_service.filter_tasks_by_status("OPEN")
    open_tasks = task_service.filtered_tasks
    tasks_recos = []
    for open_task in open_tasks:
        tasks_recos.append((open_task.uid, open_task.text))
    return [t for t in tasks_recos if incomplete in t[0]]


def get_sub_tasks(ctx, args, incomplete):
    found_task = task_service.get_task_by_id(args[1])
    tasks_recos = []
    if len(found_task.sub_tasks) > 0:
        for sub_task in found_task.sub_tasks:
            tasks_recos.append((sub_task.uid, sub_task.text))
        return [t for t in tasks_recos if incomplete in t[0]]
    else:
        return "0"


def get_status(ctx, args, incomplete):
    status = [("OPEN", "OPEN"), ("CANCELED", "CANCELED"), ("FINISHED", "FINISHED"), ("HOLD", "HOLD")]
    return [s for s in status if incomplete in s[0]]


@cli.command()
@click.argument("uid", type=click.STRING, autocompletion=get_open_tasks)
def task(uid):
    found_task = task_service.get_task_by_id(uid)
    if found_task:
        task_view = TaskView(found_task, None)
        click.echo(task_view.detail_view())
    else:
        click.echo("No Task found with uid {}".format(uid))


@cli.command()
@click.argument("uid", type=click.STRING, autocompletion=get_open_tasks)
def edit_task(uid):
    found_task = task_service.get_task_by_id(uid)
    if found_task:
        task_view = TaskView(found_task, None)
        altered_text = click.edit(task_view.detail_view())
        if altered_text:
            task_view.parse_and_alter(altered_text)
            task_service.save_tasks()
        else:
            click.echo("No changes made on task")
    else:
        click.echo("No Task found with uid {}".format(uid))


@cli.command()
@click.argument("uid", type=click.STRING, autocompletion=get_open_tasks)
@click.option("--text", prompt="Text", help="Text of the new sub task")
def add_sub_task(uid, text):
    found_task = task_service.get_task_by_id(uid)
    if found_task:
        sub_task = Task(text)
        found_task.add_sub_task(sub_task)
        task_service.save_tasks()
        click.echo("Sub Task added for {}".format(uid))
    else:
        click.echo("No Task found with number {}".format(uid))


@cli.command()
@click.argument("uid", type=click.STRING, autocompletion=get_open_tasks)
@click.argument("note", type=click.STRING)
def add_note(uid, note):
    found_task = task_service.get_task_by_id(uid)
    if found_task:
        found_task.add_note(note)
        task_service.save_tasks()
        click.echo("Note added for {}".format(uid))
    else:
        click.echo("No Task found with number {}".format(uid))


@cli.command()
@click.argument("uid", type=click.STRING, autocompletion=get_open_tasks)
@click.argument("sub_uid", type=click.STRING, autocompletion=get_sub_tasks)
@click.argument("status", type=click.STRING, autocompletion=get_status)
def change_status_sub_task(uid, sub_uid, status):
    task_uid_to_change_status_for = uid
    if sub_uid != '0':
        task_uid_to_change_status_for = sub_uid
    task = task_service.get_task_by_id(task_uid_to_change_status_for)
    if task:
        task.change_status(status)
        task_service.save_tasks()
    else:
        click.echo("No Task found with uid {}".format(uid))


@cli.command()
@click.argument("uid", type=click.STRING, autocompletion=get_open_tasks)
@click.argument("status", type=click.STRING, autocompletion=get_status)
def change_status_task(uid, status):
    task = task_service.get_task_by_id(uid)
    if task:
        task.change_status(status)
        task_service.save_tasks()
    else:
        click.echo("No Task found with uid {}".format(uid))


@cli.command()
@click.option("--uid", prompt="task id", help="Task id to change status for")
@click.option("--status", prompt="status", help="OPEN, CANCELED, CLOSED")
def change_status(uid, status):
    task = task_service.get_task_by_id(uid)
    if task:
        task.change_status(status)
        task_service.save_tasks()
    else:
        click.echo("No Task found with uid {}".format(uid))


@cli.command()
@click.option("--status", help="OPEN, CANCELED, FINISHED", default="OPEN")
@click.option("--from_date", help="Date Format: 23.5.2019")
@click.option("--query", help="Search Query")
@click.option("--all/--not-all", default=False)
@click.option("--show_uid/--not-show-uid", default=False)
def tasks(status, from_date, query, all, show_uid):
    logger.debug("tasks filter: status {}, from_date {}, query {}".format(status, from_date, query))

    if not all:
        if from_date:
            print(from_date)
            task_service.filter_tasks_by_from_date(datetime.strptime(from_date, "%d.%m.%Y"))
        if status:
            task_service.filter_tasks_by_status(status)
        if query:
            task_service.filter_tasks_by_text_query(query)
        tasks_view = TasksView(task_service.filtered_tasks)
    else:
        tasks_view = TasksView(task_service.tasks)

    if show_uid:
        click.echo(tasks_view.simple_table_view_with_uid())
    else:
        click.echo(tasks_view.simple_table_view())

    click.echo("Found {} Tasks".format(len(tasks_view.task_views)))


@cli.command()
@click.option("--uid", prompt="task id", help="Task id for task to get deleted")
def delete_task(uid):
    task = task_service.delete_task_by_id(uid)
    if task:
        click.echo("Task {} deleted".format(task.uid))
    else:
        click.echo("No Task found with uid {}".format(uid))


@cli.command()
@click.option("--text", prompt="Text", help="Text of the new Task")
def add_task(text):
    task_service.create_task(text)
    task_service.save_tasks()
    task_service.filter_tasks_by_status("OPEN")
    found_tasks = task_service.filtered_tasks
    tasks_view = TasksView(found_tasks)
    click.echo(tasks_view.simple_table_view())
