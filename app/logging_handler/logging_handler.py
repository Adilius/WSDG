import os
from pathlib import Path
from datetime import datetime


class loghandler:
    def __init__(self):
        self.root_path = os.getcwd()
        self.path_to_data = "app/data/"
        self.file_name = "app.log"
        self.init()

    def init(self):

        # Create directory
        if not Path(
            os.path.join(self.root_path, "app/data/")
        ):  # Check if it does not exist
            os.makedirs(os.path.join(self.root_path, "app/data/"))  # Create directory

        # Create file
        if not Path(os.path.join(self.root_path, f"app/data/{self.file_name}")):
            log_file = open(
                os.path.join(self.root_path, "app/data/", self.file_name),
                encoding="utf-8",
            )  # Create file
            log_file.close()

    # Writes log to file
    def write_log(self, text: str):

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = open(
            os.path.join(self.root_path, "app/data/", self.file_name),
            "a",
            encoding="utf-8",
        )  # Open file
        log = time + " | " + text
        log_file.write(log + "\n")
        log_file.close()
        return log

    # Prints log to terminal and writes to file
    def print_log(self, text: str):
        log = self.write_log(text)
        print(log)
