"""
Module to handle all logging in the program
"""

import logging
import sys

# Logging formatter supporting colorized output
class LogFormatter(logging.Formatter):

    # Color codes for each logging level
    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m",  # Purple
        logging.ERROR: "\033[1;31m",  # Red
        logging.WARNING: "\033[1;33m",  # Yellow
        logging.INFO: "\033[0;37m",  # White
        logging.DEBUG: "\033[1;34m",  # Blue
        9: "\033[1;32m",  # Green - DEBUGV level
    }

    RESET_CODE = "\033[0m"

    def __init__(self, color, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)
        self.color = color

    def format(self, record, *args, **kwargs):
        if self.color == True and record.levelno in self.COLOR_CODES:
            record.color_on = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on = ""
            record.color_off = ""
        return super(LogFormatter, self).format(record, *args, **kwargs)


# Setup logging
def setup_logging(logfile_file, log_level):

    # Add DEBUGV to logging
    logging.addLevelName(9, "DEBUGV")

    # Create logger
    logger = logging.getLogger()

    # Set log line template
    log_line_string_format = (
        "%(color_on)s%(asctime)s %(levelname)s: %(message)s%(color_off)s"
    )
    log_line_date_format = "%Y-%m-%d %H:%M:%S"

    # Console handler
    logger.setLevel(log_level)  # Set console log level
    console_handler = logging.StreamHandler(
        sys.stdout
    )  # Setup StreamHandler (Prints to console)
    console_formatter = LogFormatter(
        fmt=log_line_string_format, datefmt=log_line_date_format, color=True
    )  # Create formatter
    console_handler.setFormatter(console_formatter)  # Set formatter
    logger.addHandler(console_handler)  # Add to logger

    # Log file handler
    try:
        logfile_handler = logging.FileHandler(logfile_file)
    except Exception as exception:
        print("Failed to set up log file: %s \n Exiting..." % str(exception))
        sys.exit()

    if log_level in ["DEBUGV", "DEBUG"]:
        logfile_handler.setLevel(
            "INFO"
        )  # Never save logging level debug and below log to file
    else:
        logfile_handler.setLevel(log_level)
    logfile_formatter = LogFormatter(
        fmt=log_line_string_format, datefmt=log_line_date_format, color=False
    )  # Create formatter
    logfile_handler.setFormatter(logfile_formatter)  # Set formatter
    logger.addHandler(logfile_handler)  # Add to logger

    # Success
    return True
