import click
import os

from src.conf import Conf
from src.domain.Task import Task
from src.portadapter.out.TaskView import TaskView
from src.portadapter.out.TasksView import TasksView
from src.portadapter.out.logger import init as init_logger
from src.service.TaskService import TaskService

logger = init_logger("src.portadapter.out.commands")


class Environment(object):
    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug
        conf = Conf(logbuch_path=os.path.expanduser('~') + "/.logbuch", task_repo_file_path="/data/current.json")
        logger.debug("Initialize TaskService")
        self.task_service = TaskService(conf)


pass_environment = click.make_pass_decorator(Environment, ensure=True)
env = Environment()


@click.group()
@click.pass_context
def cli(ctx):
    ctx.object = env
    """Logbuch"""


def get_open_tasks(ctx, args, incomplete):
    env.task_service.filter_tasks_by_status("OPEN")
    open_tasks = env.task_service.filtered_tasks
    tasks_recos = []
    for open_task in open_tasks:
        tasks_recos.append((open_task.uid, open_task.text))
    return [t for t in tasks_recos if incomplete in t[0]]


def get_sub_tasks(ctx, args, incomplete):
    found_task = env.task_service.get_task_by_id(args[1])
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
@pass_environment
def edit_task(env, uid):
    found_task = env.task_service.get_task_by_id(uid)
    if found_task:
        task_view = TaskView(found_task)
        altered_text = click.edit(task_view.detail_view())
        if altered_text:
            task_view.parse_and_alter(altered_text)
            env.task_service.save_tasks()
        else:
            click.echo("No changes made on task")
    else:
        click.echo("No Task found with uid {}".format(uid))


@cli.command()
@click.argument("uid", type=click.STRING, autocompletion=get_open_tasks)
@click.option("--text", prompt="Text", help="Text of the new sub task")
@pass_environment
def add_sub_task(env, uid, text):
    found_task = env.task_service.get_task_by_id(uid)
    if found_task:
        sub_task = Task(text)
        found_task.add_sub_task(sub_task)
        env.task_service.save_tasks()
        click.echo("Sub Task added for {}".format(uid))
    else:
        click.echo("No Task found with number {}".format(uid))


@cli.command()
@click.argument("uid", type=click.STRING, autocompletion=get_open_tasks)
@click.argument("note", type=click.STRING)
@pass_environment
def add_note(env, uid, note):
    found_task = env.task_service.get_task_by_id(uid)
    if found_task:
        found_task.add_note(note)
        env.task_service.save_tasks()
        click.echo("Note added for {}".format(uid))
    else:
        click.echo("No Task found with number {}".format(uid))


@cli.command()
@click.argument("uid", type=click.STRING, autocompletion=get_open_tasks)
@click.argument("sub_uid", type=click.STRING, autocompletion=get_sub_tasks)
@click.argument("status", type=click.STRING, autocompletion=get_status)
@pass_environment
def change_status_sub_task(env, uid, sub_uid, status):
    task_uid_to_change_status_for = uid
    if sub_uid != '0':
        task_uid_to_change_status_for = sub_uid
    task = env.task_service.get_task_by_id(task_uid_to_change_status_for)
    if task:
        task.change_status(status)
        env.task_service.save_tasks()
    else:
        click.echo("No Task found with uid {}".format(uid))


@cli.command()
@click.argument("uid", type=click.STRING, autocompletion=get_open_tasks)
@click.argument("status", type=click.STRING, autocompletion=get_status)
@pass_environment
def change_status_task(env, uid, status):
    task = env.task_service.get_task_by_id(uid)
    if task:
        task.change_status(status)
        env.task_service.save_tasks()
    else:
        click.echo("No Task found with uid {}".format(uid))


@cli.command()
@click.option("--uid", prompt="task id", help="Task id for task to get deleted")
@pass_environment
def delete_task(env, uid):
    task = env.task_service.delete_task_by_id(uid)
    if task:
        click.echo("Task {} deleted".format(task.uid))
    else:
        click.echo("No Task found with uid {}".format(uid))


@cli.command()
@click.option("--text", prompt="Text", help="Text of the new Task")
@pass_environment
def add_task(env, text):
    env.task_service.create_task(text)
    env.task_service.save_tasks()
    env.task_service.filter_tasks_by_status("OPEN")
    found_tasks = env.task_service.filtered_tasks
    tasks_view = TasksView(found_tasks)
    click.echo(tasks_view.simple_table_view())
