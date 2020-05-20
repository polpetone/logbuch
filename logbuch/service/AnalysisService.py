from logbuch.service.TaskService import TaskService
from logbuch.service.TermService import TermService


class AnalysisService:

    def __init__(self, task_service: TaskService):
        self.task_service = task_service
        self.term_service = TermService(task_service.load_tasks())

    def get_most_used_terms(self):
        return self.term_service.get_most_used_terms()
