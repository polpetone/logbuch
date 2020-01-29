class LogFileService:

    def __init__(self, log_file_adapter):
        self.log_file_adapter = log_file_adapter

    def get_log_files(self, path: str):
        return self.log_file_adapter.parse_log_files(path)
