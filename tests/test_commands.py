from unittest import TestCase
from click.testing import CliRunner
from src.portadapter.out.commands import tasks


class TestCommands(TestCase):

    def test_tasks(self):
        runner = CliRunner()
        result = runner.invoke(tasks)
        print(result)
        print(result.output)
