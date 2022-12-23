"""
Main module to run program
"""
import json
import sys
import time

from datetime import datetime
import argparse
import logging
import os
from pathlib import Path
import requests

from app.enviroment_handler import enviroment_handler
from app.logging_handler import logging_handler
from app.http_handler import http_handler


def get_drop_time(response_dict):
    """
    Params: Airplane unix time from supply drop response
    Returns: days, hours, minutes, seconds until next drop using Weekly Supply Drop epoch time
    """
    airplane_time = response_dict["nextDropTime"]
    current_time = round(time.time())
    time_difference = int(airplane_time - current_time)
    days = time_difference // 86400
    hours = (time_difference - days * 86400) // 3600
    minutes = (time_difference - days * 86400 - hours * 3600) // 60
    seconds = time_difference - days * 86400 - hours * 3600 - minutes * 60
    return days, hours, minutes, seconds

def get_supply_drop_status_creates(response_dict):
    """
    Params: Response from supply drop request in dict
    Returns: Number of creates avaliable for weekly, activity, and levelup
    """
    weekly_avaliable, activity_avaliable, levelup_avaliable = 0, 0, 0
    weekly_avaliable = int(response_dict["crateTypes"][0]["openableCount"])
    activity_avaliable = int(response_dict["crateTypes"][1]["openableCount"])
    levelup_avaliable = int(response_dict["crateTypes"][2]["openableCount"])
    return weekly_avaliable, activity_avaliable, levelup_avaliable

def print_supply_drop_status(response_supply_text):
    """
    Params: Response from supply drop request
    Prints all supply drop status
    """
    response_dict = json.loads(response_supply_text)
    (
        weekly_avaliable,
        activity_avaliable,
        levelup_avaliable,
    ) = get_supply_drop_status_creates(response_dict)
    days, hours, minutes, seconds = map(str, get_drop_time(response_dict))
    activity_drop_counter = str(response_dict["crateTypes"][1]["nextResupplyIn"])
    level_up_progress = str(response_dict["crateTypes"][2]["progress"])[2:4]

    logging.debug(
        f"""
------ SUPPLY DROP STATUS ------
{datetime.now().strftime("Time: %Y-%m-%d %H:%M:%S")}
Weekly drop avaliable: {weekly_avaliable}
Weekly drop time left: {days} days | {hours} hours | {minutes} minutes | {seconds} seconds
Activity drop avaliable: {activity_avaliable}
Activity drop in: {activity_drop_counter} orders
Level up drop avaliable: {levelup_avaliable}
Level up drop progress: {level_up_progress}%
--------------------------------"""
    )
    return weekly_avaliable, activity_avaliable, levelup_avaliable

def parse_arguments():
    pass


def run_script(username: str, password: str):
    """
    Main function to run script
    Params: Username for Webhallen account
    Params: Password for Webhallen account
    """
    # Create a session which stores our cookie for further API requests
    session = requests.Session()

    # Login to grab cookie & get user ID for further API requests
    response, user_id = http_handler.login_request(session, username, password)

    # Call API to get supply drop status
    (
        supply_drop_status_sucess,
        supply_drop_status_response,
    ) = http_handler.supply_drop_request(session)

    # Supply drop status success. Get correct amount of supplies avaliable.
    if supply_drop_status_sucess:
        (
            weekly_avaliable,
            activity_avaliable,
            levelup_avaliable,
        ) = print_supply_drop_status(supply_drop_status_response.text)

        if weekly_avaliable >= 1:
            for _ in range(weekly_avaliable):
                http_handler.weekly_supply_drop_request(session, user_id)

        if activity_avaliable >= 1:
            for _ in range(activity_avaliable):
                http_handler.activity_supply_drop_request(session, user_id)

        if levelup_avaliable >= 1:
            for _ in range(levelup_avaliable):
                http_handler.levelup_supply_drop_request(session, user_id)

        if weekly_avaliable + activity_avaliable + levelup_avaliable == 0:
            logging.info("No supply drop avaliable.")


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Automatically grab Webhallen supply drops using HTTP requests.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-e",
        action="store",
        required=False,
        type=str,
        help="Email used to login into Webhallen",
        metavar="<email>",
        dest="email",
    )
    parser.add_argument(
        "-p",
        action="store",
        required=False,
        type=str,
        help="Password used to login into Webhallen",
        metavar="<password>",
        dest="password",
    )
    log_levels = ["DEBUGV", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    parser.add_argument(
        "-l",
        action="store",
        default="INFO",
        required=False,
        type=str,
        choices=log_levels,
        help=f"""Log level options: {log_levels}
Default value: INFO. DEBUG and below level logs will only be printed in console.
DEBUGV also prints username, password, and userid.""",
        metavar="<log level>",
        dest="log_level",
    )
    parser.add_argument(
        "-s",
        action="store",
        required=False,
        type=bool,
        help="Save and encrypt login credentials for future use. (Read README)",
        dest="store",
    )
    args = parser.parse_args()


    # Setup logging
    log_level = (args.log_level).upper()    # Get log level variable
    filename = os.path.join(Path(__file__).parent, "adiliuswsdg.log")  # Get path to log file
    logging_handler.setup_logging(logfile_file=filename, log_level=log_level)
    

    # Start enviroment handler globally
    EnvHandler = enviroment_handler.EnvHandler(email = args.email, password = args.password, store = args.store)

    # Get login variables
    webhallen_username = EnvHandler.get_variable("email")
    webhallen_password = EnvHandler.get_variable("password")

    # Run script
    run_script(webhallen_username, webhallen_password)

    # Exit
    logging.debug("AdiliusWSDG exiting.")
    sys.exit(0)
