import logging
from logging.handlers import RotatingFileHandler, SysLogHandler
import atexit

class CustomLogger:
    def __init__(self, name, filename, maxBytes=1048576, backupCount=5, use_syslog=False):
        """
        Initializes a custom logger with a RotatingFileHandler and an optional SysLogHandler (disabled by default)

        Parameters:
        - name: The name of the logger.
        - filename: Path to the log file.
        - maxBytes: Maximum file size before rotating (default is 1MB).
        - backupCount: Number of backup files to keep (default is 5).
        - use_syslog: Log messages to syslog.log in addition to the custom log file. Default is false.
        """
        self.logger = logging.getLogger(name)
        if not self.logger.hasHandlers():
            formatter = logging.Formatter("%(asctime)s - %(message)s")
            file_handler = RotatingFileHandler(filename, maxBytes=maxBytes, backupCount=backupCount)
            file_handler.setFormatter(formatter)
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(file_handler)

            # Setup syslog handler
            if use_syslog:
                syslog_handler = SysLogHandler(address='/dev/log')  # Update '/dev/log' if necessary
                syslog_handler.setFormatter(formatter)
                self.logger.addHandler(syslog_handler)

            self.logger.setLevel(logging.INFO)
            atexit.register(self.removeHandlers, file_handler, syslog_handler if use_syslog else None)

    def removeHandlers(self, file_handler, syslog_handler=None):
        """
        Removes handlers from the logger and closes them. Intended to be called at exit.
        """
        self.logger.removeHandler(file_handler)
        file_handler.close()
        if syslog_handler:
            self.logger.removeHandler(syslog_handler)
            syslog_handler.close()

    def info(self, message):
        """
        Logs an INFO level message.
        """
        self.logger.info(message)

    def debug(self, message):
        """
        Logs a DEBUG level message.
        """
        self.logger.debug(message)

    def error(self, message):
        """
        Logs an ERROR level message.
        """
        self.logger.error(message)

# Usage:
# exampleLog = CustomLogger("exampleLogger", "/tmp/example.log", 1000000, 3)
# exampleLog.info("This is a test log message.")
