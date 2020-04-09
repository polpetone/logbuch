from datetime import datetime

from src.portadapter.out.logger import init as init_logger

logger = init_logger("src.portadapter.domain.TaskView")

TASK_SEPARATOR = "######_TASK_######"


class TaskView(object):

    def __init__(self, task, select_number):
        self.task = task
        self.select_number = select_number
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
        sub_task_counter = 0
        for sub_task in task.sub_tasks:
            sub_task_counter += 1
            self.sub_task_views.append(TaskView(sub_task, sub_task_counter))

    def get_sub_task_view_by_number(self, number):
        result = [x for x in self.sub_task_views if x.select_number == number]
        if len(result) > 0:
            return result[0]
        return None

    def simple_view(self):
        template = "{0:<30}{1:<60}{2:<20}{3:<30}\n"
        sub_task_template = "{0:<30}{1:<30}{2:<60}{3:<20}{4:<30}\n"
        gap_template = "{0:<160}\n"

        out = template.format(self.date, self.shortened_text, self.status, self.status_date)

        if len(self.sub_task_views) > 0:
            out += gap_template.format(200 * ".")

        for sub_task_view in self.sub_task_views:
            out += sub_task_template.format("",
                                            sub_task_view.date,
                                            sub_task_view.shortened_text,
                                            sub_task_view.status,
                                            sub_task_view.status_date)
        return out

    def simple_view_with_uid(self):
        template = "{0:<50}{1:<30}{2:<60}{3:<20}{4:<30}\n"
        sub_task_template = "{0:<30}{1:<50}{2:<30}{3:<60}{4:<20}{5:<30}\n"
        gap_template = "{0:<160}\n"

        out = template.format(self.task.uid, self.date, self.shortened_text, self.status, self.status_date)

        if len(self.sub_task_views) > 0:
            out += gap_template.format(200 * ".")

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

        out = TASK_SEPARATOR + "\n"
        out += id_line + "\n"
        out += date_line + "\n"
        out += text_line + "\n"
        out += status_line + "\n"
        out += status_date_line + "\n  \n"

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
