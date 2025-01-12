import logging
from io import StringIO

class Progress:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(__name__)

        self.log_file_path = None
        self.log_stream = None
        self.log_flush = None

        self.init = False

    def init_progress(self, log_file_path: str):
        self.init = True
        # step 1. User & log path
        self.log_file_path = log_file_path

        # step 2  prepare new handler for logger
        if not any(handler.name == "Logic: Progress [Info]" for handler in self.logger.handlers):
            self.log_stream = StringIO()
            task_log_handler = logging.StreamHandler(self.log_stream)
            task_log_handler.setLevel(logging.INFO)
            task_log_handler.name = "Logic: Progress [Info]"
            self.logger.addHandler(task_log_handler)

        # assign function for log and notification
        def flush():
            try:
                logs = self.log_stream.getvalue()
                with open(self.log_file_path, 'a') as log_file:
                    log_file.write(logs)
            except Exception as e:
                self.log_stream = StringIO()

            self.log_stream.truncate(0) # Clear the log stream after flushing
            self.log_stream.seek(0)

        self.log_flush = flush
        return True

    def flush(self):
        if self.init == False:
            return True
        if self.log_flush:
            self.log_flush()
        return True
