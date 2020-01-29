from src.portadapter.input.migration.domain.Task import Task
from src.portadapter.input.migration.domain.TaskStatus import TaskStatus
from typing import List


class TaskSymbol:
    def __init__(self, status, symbols):
        self.symbols = symbols
        self.status = status


TASK_SYMBOLS = [
    TaskSymbol(TaskStatus.OPEN, ["[]", "[ ]"]),
    TaskSymbol(TaskStatus.FINISHED, ["[x]"]),
    TaskSymbol(TaskStatus.MOVED, ["[m]"]),
    TaskSymbol(TaskStatus.CANCELED, ["[c]"])
]


def __build_task_from_raw_line(line):
    found_task_symbol = None
    raw_symbol = ""
    for task_symbol in TASK_SYMBOLS:
        for symbol in task_symbol.symbols:
            if symbol in line:
                found_task_symbol = task_symbol
                raw_symbol = symbol

    if found_task_symbol:
        return Task(found_task_symbol.status, line.replace(raw_symbol, "").strip()), None
    return None, line.strip()


def build_task_block_from_raw_lines(lines: List[str]):
    tasks = []
    for line in lines:
        task, addition = __build_task_from_raw_line(line)
        if task is not None:
            tasks.append(task)
        if addition is not None:
            if len(tasks) > 0:
                tasks[-1].append_addition(addition)
    return tasks
