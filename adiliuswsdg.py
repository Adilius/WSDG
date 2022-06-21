"""
Main module to run program
"""
import json
import sys
import time
import urllib.parse
from datetime import datetime
import argparse
import requests

from app.enviroment_handler import enviroment_handler
from app.logging_handler import logging_handler
from app.http_handler import http_handler

BASE_API_URL = "https://www.webhallen.com/api/"
CONTINIOUS_GRAB_TIME = "00:10"


def get_drop_time(airplane_time: float):
    """
    Returns days, hours, minutes, seconds until next drop using Weekly Supply Drop epoch time
    """
    current_time = round(time.time())
    time_difference = int(airplane_time - current_time)
    days = time_difference // 86400
    hours = (time_difference - days * 86400) // 3600
    minutes = (time_difference - days * 86400 - hours * 3600) // 60
    seconds = time_difference - days * 86400 - hours * 3600 - minutes * 60
    return days, hours, minutes, seconds


def weekly_supply_drop_request(session, webhallen_user_id: str):
    """
    Params: Session after login success
    Params: Webhallen User ID
    Sends request to collect weekly supply drop
    """
    url = BASE_API_URL + "supply-drop/"

    headers = {
        "referer": "https://www.webhallen.com/se/member/"
        + str(webhallen_user_id)
        + "/supply-drop"
    }

    print("Sending request to grab weekly supply drop...")
    response = session.post(url=url, headers=headers)

    # Handle bad response
    if response.status_code != 200:
        error_msg = (
            f"Error grabbing weekly supply drop. Status code: {response.status_code}"
        )
        print(error_msg)
        loghandler.print_log(error_msg)
        return

    response_json = json.loads(response.text)
    for drop in response_json["drops"]:
        name = drop["name"]
        description = drop["description"]
        loghandler.print_log(f"Grabbed supply drop {name} and got {description}")


def activity_supply_drop_request(session, webhallen_user_id: str):
    """
    Params: Session after login success
    Params: Webhallen User ID
    Sends request to collect activity supply drop
    """
    url = "https://www.webhallen.com/api/supply-drop"

    headers = {
        "authority": "www.webhallen.com",
        "origin": "https://www.webhallen.com",
        "referer": "https://www.webhallen.com/se/member/"
        + str(webhallen_user_id)
        + "/supply-drop",
    }

    data = '{"crateType":"activity"}'

    print("Sending request to grab activity supply drop...")
    response = session.post(url=url, headers=headers, data=data)

    # Handle bad response
    if response.status_code != 200:
        error_msg = (
            f"Error grabbing activity supply drop. Status code: {response.status_code}"
        )
        print(error_msg)
        loghandler.print_log(error_msg)
        return

    print(response)


def levelup_supply_drop_request(session, webhallen_user_id: str):
    """
    EXPERIMENTAL, needs configuration!
    Params: Session after login success
    Params: Webhallen User ID
    Sends request to collect level up supply drop
    """
    url = "https://www.webhallen.com/api/supply-drop"

    headers = {
        "authority": "www.webhallen.com",
        "origin": "https://www.webhallen.com",
        "referer": "https://www.webhallen.com/se/member/"
        + str(webhallen_user_id)
        + "/supply-drop",
    }

    data = '{"crateType":"level-up"}'

    print("Sending request to grab level up supply drop...")
    response = session.post(url=url, headers=headers, data=data)

    # Handle bad response
    if response.status_code != 200:
        error_msg = (
            f"Error grabbing level up supply drop. Status code: {response.status_code}"
        )
        print(error_msg)
        loghandler.print_log(error_msg)
        return

    print(response)


def grab_user_id(session):
    """
    Params: Session after login success
    Returns: Webhallen User ID
    """

    verbose = EnvHandler.get_variable("VERBOSE")
    loghandler.print_log("Grabbing Webhallen User ID from cookies")
    try:
        webhallen_auth_token = session.cookies["webhallen_auth"]
        webhallen_user_id = json.loads(urllib.parse.unquote(webhallen_auth_token))
    except KeyError:
        loghandler.print_log("Failed to get authentication token! Exiting program")
        sys.exit(1)
    else:
        loghandler.print_log(
            "Webhallen User ID: " + str(webhallen_user_id["user_id"])
            if verbose == "y"
            else "Webhallen User ID: *******"
        )

    return webhallen_user_id


def supply_drop_status(response_supply_text):
    """
    Params: Response from supply drop request
    Prints all supply drop status
    """
    response_json = json.loads(response_supply_text)
    days, hours, minutes, seconds = get_drop_time(response_json["nextDropTime"])

    weekly_avaliable, activity_avaliable, levelup_avaliable = 0, 0, 0

    weekly_avaliable = int(response_json["crateTypes"][0]["openableCount"])
    activity_avaliable = int(response_json["crateTypes"][1]["openableCount"])
    levelup_avaliable = int(response_json["crateTypes"][2]["openableCount"])

    print("------ SUPPLY DROP STATUS ------")
    print(datetime.now().strftime("Time: %Y-%m-%d %H:%M:%S"))
    print("Weekly drop avaliable:", weekly_avaliable)
    if days + hours + minutes + seconds > 1:
        print(
            "Weekly drop time left:",
            (str(days) + " days") if days > 0 else "",
            (str(hours) + " hours") if hours > 0 else "",
            (str(minutes) + " minutes") if minutes > 0 else "",
            (str(seconds) + " seconds") if seconds > 0 else "",
        )

    print("Activity drop avaliable:", activity_avaliable)
    print(
        "Activity drop in: "
        + str(response_json["crateTypes"][1]["nextResupplyIn"])
        + " drops"
    )

    print("Level up drop avaliable:", levelup_avaliable)
    print(
        "Level up drop progress: "
        + str(response_json["crateTypes"][2]["progress"])[2:4]
        + "%"
    )
    print("--------------------------------")

    return weekly_avaliable, activity_avaliable, levelup_avaliable


def run_script(username: str, password: str):
    """
    Main function to run script
    Params: Username for Webhallen account
    Params: Password for Webhallen account
    """
    session = requests.Session()
    http_handler.login_request(session, username, password)
    user_id = grab_user_id(session)
    response_supply = http_handler.supply_drop_request(session)
    weekly_avaliable, activity_avaliable, levelup_avaliable = supply_drop_status(
        response_supply.text
    )
    if weekly_avaliable + activity_avaliable + levelup_avaliable >= 1:
        print("Supply drop avaliable.")

        for _ in range(weekly_avaliable):
            weekly_supply_drop_request(session, user_id)

        for _ in range(activity_avaliable):
            activity_supply_drop_request(session, user_id)

        for _ in range(levelup_avaliable):
            levelup_supply_drop_request(session, user_id)
    else:
        loghandler.print_log("No supply drop avaliable.")




def main():
    """
    Initialize start up settings
    """

    # Get login variables
    webhallen_username = EnvHandler.get_variable("WEBHALLEN_USERNAME")
    webhallen_password = EnvHandler.get_variable("WEBHALLEN_PASSWORD")

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Automatically grab Webhallen supply drops using HTTP requests."
    )
    parser.add_argument(
        "-c",
        "--continuous",
        action="store_true",
        help=f"Run script in background and continuously grab drops at {CONTINIOUS_GRAB_TIME}",
    )
    args = parser.parse_args()

    # Continiously running the program
    if args.continuous:

        time_until_repeat = 86400
        timer = 0

        # Run once first
        run_script(webhallen_username, webhallen_password)

        while True:
            seconds_left = time_until_repeat-timer
            time_left = datetime.utcfromtimestamp(seconds_left).strftime("%H:%M:%S")
            print(f"Continuously running script: {time_left} seconds until next run",end="\r")

            # 24 hours has passed
            if timer == time_until_repeat:
                run_script(webhallen_username, webhallen_password)
                timer = 0

            # Sleep 1 second
            time.sleep(1)

            # Increment timer
            timer += 1

    # Run one time
    else:
        run_script(webhallen_username, webhallen_password)

        loghandler.print_log("AdiliusWSDG exiting.")
        sys.exit(1)

if __name__ == "__main__":

    # Start logging handler globally
    loghandler = logging_handler.LogHandler()
    loghandler.print_log("AdiliusWSDG starting.")

    # Start enviroment handler globally
    EnvHandler = enviroment_handler.EnvHandler()

    # Run start up script
    main()
