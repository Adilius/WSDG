"""
Module to handle all logging in the program
"""

import os
from pathlib import Path
from datetime import datetime


class LogHandler:
    """
    Class to handle logging
    """

    def __init__(self):
        self.root_path = os.getcwd()
        self.file_name = "app.log"
        self.init()

    def init(self):
        """
        Init function. Creates  log file if it does not already exist.
        """

        if not Path(os.path.join(self.root_path, self.file_name)):
            with open(os.path.join(self.root_path, self.file_name), encoding="utf-8"):
                pass

    def write_log(self, text: str):
        """
        Writes text to log file.
        """
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(
            os.path.join(self.root_path, self.file_name), "a", encoding="utf-8"
        ) as log_file:
            log = time + " | " + text
            log_file.write(f"{log}\n")
        return log

    def print_log(self, text: str):
        """
        Writes text to log file.
        Prints text to console.
        """
        log = self.write_log(text)
        print(log)
