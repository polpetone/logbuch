import click
from src.portadapter.cli import pass_environment
from src.portadapter.out.TaskView import TaskView


@click.command()
@click.argument("uid", type=click.STRING, autocompletion=get_open_tasks)
@pass_environment
def task(env, uid):
    found_task = env.task_service.get_task_by_id(uid)
    if found_task:
        task_view = TaskView(found_task)
        click.echo(task_view.detail_view())
    else:
        click.echo("No Task found with uid {}".format(uid))
