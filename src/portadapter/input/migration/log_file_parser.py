from datetime import datetime
from glob import glob
from src.portadapter.input.migration.task_parser import build_task_block_from_raw_lines
from src.portadapter.input.migration.domain.LogFile import LogFile


class LogFileParser:

    def parse_log_files(self, path):
        files = self.get_all_log_files(path)
        logs = []
        for f in files:
            log = self.parse_log_file(f)
            logs.append(log)
        return logs

    def get_all_log_files(self, path):
        files = glob(path + "/**/*-log", recursive=True)
        return files

    def parse_log_file(self, f):
        with open(f, 'r', encoding="UTF-8") as log_file:
            raw = log_file.readlines()
            date_string = self.get_date_from_file_name(log_file.name)
            location = self.find_location(raw)
            task_blocks = self.extract_task_blocks_from_raw_lines(raw)
            tasks = self.make_tasks_with_subs_from_task_blocks(task_blocks)
            date = datetime.strptime(date_string, "%d-%m-%Y")
            for task in tasks:
                task.set_date(date)
            log = LogFile(date, location, tasks)
        return log

    def make_tasks_with_subs_from_task_blocks(self, task_blocks):
        tasks = []
        for task_block in task_blocks:
            task = task_block[0]
            for t in range(1, len(task_block)):
                task.append_sub_task(task_block[t])
            tasks.append(task)
        return tasks

    def get_date_from_file_name(self, absolute_path: str):
        raw = absolute_path.split("/")
        file_name = raw[len(raw)-1][:-4]
        return file_name

    def find_date(self, raw_lines):
        if len(raw_lines) > 0:
            return raw_lines[0].strip()
        return "unknown"

    def find_location(self, raw_lines):
        token = "location:"
        if len(raw_lines) > 4:
            for x in range(0, 5):
                if token in raw_lines[x]:
                    location_raw = raw_lines[x].split(":")
                    if len(location_raw) > 1:
                        return location_raw[1].strip()
        return "unknown"

    def extract_task_blocks_from_raw_lines(self, raw_lines):
        task_blocks = []
        for i in range(0, len(raw_lines)):
            if len(raw_lines[i]) > 0:
                if "[" in raw_lines[i][0]:
                    task_block_lines = [raw_lines[i]]
                    i += 1
                    while i < len(raw_lines) and raw_lines[i].strip() != "":
                        task_block_lines.append(raw_lines[i])
                        i += 1
                    task_block = build_task_block_from_raw_lines(task_block_lines)
                    task_blocks.append(task_block)
        return task_blocks
