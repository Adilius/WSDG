"""
Main module to run program
"""
from calendar import week
import json
import sys
import time
import urllib.parse
from datetime import datetime
import argparse
import requests
import logging
import os
from pathlib import Path

from app.enviroment_handler import enviroment_handler
from app.logging_handler import logging_handler
from app.http_handler import http_handler

def grab_user_id(session):
    """
    Params: Session after login success
    Returns: Webhallen User ID
    """
    logging.debug("Grabbing Webhallen User ID from cookies")
    try:
        webhallen_auth_token = session.cookies["webhallen_auth"]
        webhallen_user_id = json.loads(urllib.parse.unquote(webhallen_auth_token))
    except KeyError:
        logging.debug("Failed to get authentication token! Exiting program")
        sys.exit(1)
    else:
        logging.debugv("Webhallen User ID: " + str(webhallen_user_id["user_id"]))
    return webhallen_user_id

def get_drop_time(response_dict):
    """
    Params: Airplane unix time from supply drop response
    Returns: days, hours, minutes, seconds until next drop using Weekly Supply Drop epoch time
    """
    airplane_time= response_dict["nextDropTime"]
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
    weekly_avaliable, activity_avaliable, levelup_avaliable = get_supply_drop_status_creates(response_dict)
    days, hours, minutes, seconds = get_drop_time(response_dict)


    logging.debug(f"""
------ SUPPLY DROP STATUS ------
{datetime.now().strftime("Time: %Y-%m-%d %H:%M:%S")}
Weekly drop avaliable: {str(weekly_avaliable)}
{("Weekly drop time left: " +
((str(days) + " days") if days > 0 else "") +
((str(hours) + " hours ") if hours > 0 else "") +
((str(minutes) + " minutes ") if minutes > 0 else "") +
((str(seconds) + " seconds") if seconds > 0 else ""))
if days + hours + minutes + seconds > 1 else ""}
Activity drop avaliable: {str(activity_avaliable)}
Activity drop in: {str(response_dict["crateTypes"][1]["nextResupplyIn"])} orders
Level up drop avaliable: {str(levelup_avaliable)}
Level up drop progress: {str(response_dict["crateTypes"][2]["progress"])[2:4]}%
--------------------------------""")
    return weekly_avaliable, activity_avaliable, levelup_avaliable
    

def run_script(username: str, password: str):
    """
    Main function to run script
    Params: Username for Webhallen account
    Params: Password for Webhallen account
    """
    # Create a session which stores our cookie for further API requests
    session = requests.Session()

    # Login to grab cookie & get user ID for further API requests
    http_handler.login_request(session, username, password)
    user_id = grab_user_id(session)

    # Call API to get supply drop status
    supply_drop_status_sucess, supply_drop_status_response = http_handler.supply_drop_request(session)

    # Supply drop status success. Get correct amount of supplies avaliable.
    if supply_drop_status_sucess:
        weekly_avaliable, activity_avaliable, levelup_avaliable = print_supply_drop_status(supply_drop_status_response.text)    

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
            logging.debug("No supply drop avaliable.")

def main():
    """
    Initialize start up settings
    """

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Automatically grab Webhallen supply drops using HTTP requests.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    log_levels = ['DEBUGV', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    parser.add_argument(
        "-l",
        "--log-level",
        action="store",
        default='INFO',
        required=False,
        type=str,
        choices=log_levels,
        help=f"Log level options: {log_levels}\nDEBUG and below level logs will only be printed in console.\nDEBUGV also prints username, password, and userid.",
        metavar="<log level>",
        dest="log_level"
    )
    args = parser.parse_args()

    # Get log level variable
    log_level = (args.log_level).upper()

    # Setup logging
    filename = os.path.join(Path(__file__).parent, 'adiliuswsdg.log')   # Get path to log file
    if (not logging_handler.setup_logging(logfile_file=filename, log_level=log_level)):
        print("Failed to setup logging.")
       
    # Log some messages
    #logging.debugv("Debugv message")
    #logging.debug("Debug message")
    #logging.info("Info message")
    #logging.warning("Warning message")
    #logging.error("Error message")
    #logging.critical("Critical message")
    #logging.debug('AdiliusWSDG starting.')

    # Get login variables
    webhallen_username = EnvHandler.get_variable("WEBHALLEN_USERNAME")
    webhallen_password = EnvHandler.get_variable("WEBHALLEN_PASSWORD")

    # Run script
    run_script(webhallen_username, webhallen_password)

    # Exit
    logging.debug("AdiliusWSDG exiting.")
    sys.exit(1)


# Run start up script
if __name__ == "__main__":

    # Start enviroment handler globally
    EnvHandler = enviroment_handler.EnvHandler()

    main()
