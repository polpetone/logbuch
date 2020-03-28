from unittest import TestCase

from build.lib.src.domain.Task import Task


class TestTask(TestCase):

    def test_create_task(self):
        task = Task("some task")
        assert task.text == "some task"

    def test_add_note(self):
        task = Task("some task")
        task.add_note("a note")

        assert task.notes[0] == "a note"
