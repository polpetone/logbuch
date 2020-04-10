from datetime import datetime
import click
from src.portadapter.cli import pass_environment
from src.portadapter.cli import logger
from src.portadapter.out.TasksView import TasksView


@click.command()
@click.option("--status", help="OPEN, CANCELED, FINISHED, HOLD", default="OPEN")
@click.option("--from_date", help="Date Format: 23-5-2019. Filter tasks by status date")
@click.option("--query", help="Search Query")
@click.option("--all/--not-all", default=False)
@click.option("--show_uid/--not-show-uid", default=False)
@pass_environment
def tasks(env, status, from_date, query, all, show_uid):
    logger.debug("tasks filter: status {}, from_date {}, query {}".format(status, from_date, query))

    if not all:
        if from_date:
            env.task_service.filter_tasks_by_from_status_date(datetime.strptime(from_date, "%d-%m-%Y"))
        if status:
            env.task_service.filter_tasks_by_status(status)
        if query:
            env.task_service.filter_tasks_by_text_query(query)
        env.task_service.sort_filtered_tasks_by_status_date()
        tasks_view = TasksView(env.task_service.filtered_tasks)
    else:
        env.task_service.sort_filtered_tasks_by_status_date()
        tasks_view = TasksView(env.task_service.filtered_tasks)

    if show_uid:
        click.echo(tasks_view.simple_table_view_with_uid())
    else:
        click.echo(tasks_view.simple_table_view(gab_char='.'))

    click.echo("Found {} Tasks".format(len(tasks_view.task_views)))
