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

    logger.setLevel(log_level)  # Set console log level

    # Setup logging to console
    console_handler = create_console_handler(log_line_string_format, log_line_date_format)
    if console_handler:
        logger.addHandler(console_handler)

    # Setup logging to file
    file_handler = create_file_handler(log_line_string_format, log_line_date_format, logfile_file, log_level)
    logger.addHandler(file_handler)  # Add to logger


def create_console_handler(log_line_string_format, log_line_date_format):
    """
    Create StreamHandler (Prints to console)
    """
    try:
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = LogFormatter(fmt=log_line_string_format, datefmt=log_line_date_format, color=True)
        console_handler.setFormatter(console_formatter)
        return console_handler
    except Exception as exception:
        print(f"Failed to setup console logging: {exception}")
        return False
    
    
def create_file_handler(log_line_string_format, log_line_date_format, logfile_file, log_level):
    """
    Create FileHandler (Prints to file)
    """
    try:
        logfile_handler = logging.FileHandler(logfile_file)

        # Never save logging level debug and below log to file
        if log_level in ["DEBUGV", "DEBUG"]:
            logfile_handler.setLevel("INFO")  
        else:
            logfile_handler.setLevel(log_level)
        
        logfile_formatter = LogFormatter(fmt=log_line_string_format, datefmt=log_line_date_format, color=False)
        logfile_handler.setFormatter(logfile_formatter)

        return logfile_handler
    except Exception as exception:
        logging.error(f"Failed to set up log file: {str(exception)}")
        return False
