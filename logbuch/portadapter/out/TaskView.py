from datetime import datetime

from logbuch.portadapter.out.logger import init as init_logger

logger = init_logger("logbuch.portadapter.domain.TaskView")

TASK_SEPARATOR = "######_TASK_######"


class TaskView(object):

    def __init__(self, task):
        self.task = task
        if task.date:
            self.date = task.date.strftime("%d-%m-%Y %H:%M:%S")
        else:
            self.date = ""
        self.text = task.text
        self.shortened_text = task.text[:55]
        self.status = task.status.status
        if task.status.date:
            self.status_date = task.status.date.strftime("%d-%m-%Y %H:%M:%S")
        else:
            self.status_date = ""
        self.sub_task_views = []

        for sub_task in task.sub_tasks:
            self.sub_task_views.append(TaskView(sub_task))
        self.notes = "\n".join(self.task.notes)

    def view_with_notes(self, gab_char=""):
        template = "{0:<30}{1:<80}{2:<10}{3:<30}\n"
        note_template = "{0:<30}{1:<80}{2:<20}{3:<30}\n"
        sub_task_template = "{0:<30}{1:<30}{2:<80}{3:<10}{4:<30}\n"
        sub_task_note_template = "{0:<30}{1:<30}{2:<80}{3:<20}{4:<30}\n"
        gap_template = "{0:<160}\n"

        out = template.format(self.date, self.shortened_text, self.status, self.status_date)

        for note in self.task.notes:
            note_out = note_template.format("", note, "", "")
            out += note_out

        if len(self.sub_task_views) > 0:
            out += gap_template.format(180 * gab_char)

        for sub_task_view in self.sub_task_views:
            out += sub_task_template.format("",
                                            sub_task_view.date,
                                            sub_task_view.shortened_text,
                                            sub_task_view.status,
                                            sub_task_view.status_date)
            for note in sub_task_view.task.notes:
                note_out = sub_task_note_template.format("", "", note, "", "")
                out += note_out

        return out

    def simple_view_with_uid(self, gab_char=""):
        template = "{0:<50}{1:<30}{2:<80}{3:<10}{4:<30}\n"
        sub_task_template = "{0:<30}{1:<50}{2:<30}{3:<80}{4:<10}{5:<30}\n"
        gap_template = "{0:<160}\n"

        out = template.format(self.task.uid, self.date, self.shortened_text, self.status, self.status_date)

        if len(self.sub_task_views) > 0:
            out += gap_template.format(180 * gab_char)

        for sub_task_view in self.sub_task_views:
            out += sub_task_template.format("",
                                            sub_task_view.task.uid,
                                            sub_task_view.date,
                                            sub_task_view.shortened_text,
                                            sub_task_view.status,
                                            sub_task_view.status_date)
        return out

    def detail_view(self):

        id_line = "        uid: {}".format(self.task.uid)
        date_line = "       task_date: {}".format(self.date)
        text_line = "       text: {}".format(self.task.text)
        status_line = "     task_status: {}".format(self.status)
        status_date_line = "status_date: {}".format(self.status_date)
        notes_lines = "notes: \n{}".format(self.notes)

        out = TASK_SEPARATOR + "\n"
        out += id_line + "\n"
        out += date_line + "\n"
        out += text_line + "\n"
        out += status_line + "\n"
        out += status_date_line + "\n"
        out += notes_lines + "\n  \n"

        sub_task_out = ""

        for sub_task_view in self.sub_task_views:
            sub_task_out += sub_task_view.detail_view()

        return out + sub_task_out

    def alter_task(self, task_to_alter, task_block):

        for line in task_block:

            if "text:" in line:
                logger.debug("alter text")
                text_line = line.split("text:")
                task_to_alter.text = text_line[1].strip()

            if "task_date:" in line:
                logger.debug("alter task_date")
                text_line = line.split("task_date:")
                date_string = text_line[1].strip()
                task_to_alter.date = datetime.strptime(date_string, "%d-%m-%Y %H:%M:%S")

            if "task_status:" in line:
                logger.debug("alter task_status")
                text_line = line.split("task_status:")
                status = text_line[1].strip()
                task_to_alter.status.status = status

            if "status_date:" in line:
                logger.debug("alter status_date")
                text_line = line.split("status_date:")
                date_string = text_line[1].strip()
                task_to_alter.status.date = datetime.strptime(date_string, "%d-%m-%Y %H:%M:%S")

    def parse_and_alter(self, detail_view_string):
        raw_task_blocks = detail_view_string.split(TASK_SEPARATOR)

        unclean_task_blocks = []
        for raw_task_block in raw_task_blocks:
            unclean_task_blocks.append(raw_task_block.split('\n'))

        task_blocks = []
        for task_block in unclean_task_blocks:
            if len(task_block) > 4:
                task_blocks.append(task_block)

        logger.debug(task_blocks)
        self.alter_task(self.task, task_blocks[0])

        if len(task_blocks) > 1:
            sub_task_index = 0
            for sub_task_block in task_blocks[1:]:
                self.alter_task(self.task.sub_tasks[sub_task_index], sub_task_block)
                sub_task_index += 1
