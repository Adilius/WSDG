"""
Module to handle all HTTP requests sent to Webhallen
"""
import json
import sys

from ..logging_handler import logging_handler
from ..enviroment_handler import enviroment_handler

LOGIN_URL = "https://www.webhallen.com/api/login"
SUPPLY_DROP_URL = "https://www.webhallen.com/api/supply-drop"


def login_request(session, webhallen_username: str, webhallen_password: str):
    """
    Sends request to login to webhallen
    Params: A new requests session
    Returns: Response
    """
    loghandler = logging_handler.LogHandler()
    env_handler = enviroment_handler.EnvHandler()
    verbose = env_handler.get_variable("VERBOSE")

    headers = {"Content-Type": "application/json"}
    body = json.dumps({"username": webhallen_username, "password": webhallen_password})
    loghandler.print_log("Sending login request...")
    loghandler.print_log(
        "Webhallen username: " + webhallen_username
        if verbose == "y"
        else "Webhallen username: *******"
    )
    loghandler.print_log(
        "Webhallen password: " + webhallen_password
        if verbose == "y"
        else "Webhallen password: *******"
    )

    response = session.post(url=LOGIN_URL, headers=headers, data=body)
    if response.status_code == 403:
        loghandler.print_log("Forbidden access: Status code 403")
        loghandler.print_log("Possibly wrongly set username and password")
        loghandler.print_log("Exiting...")
        sys.exit()
    elif response.status_code != 200:
        loghandler.print_log(f"Status code: {response.status_code}")
        loghandler.print_log("Login failed. Exiting...")
        sys.exit()

    loghandler.print_log("Login success!")
    return response


def supply_drop_request(session):
    """
    Sends request to webhallen supply drop status API
    Params: A new requests session
    Returns: Response
    """
    loghandler = logging_handler.LogHandler()
    loghandler.print_log("Sending supply drop status request...")
    response = session.get(url=SUPPLY_DROP_URL)

    if response.status_code != 200:
        loghandler.print_log(f"Status code: {response.status_code}")
        loghandler.print_log("Supply drop page failed. Exiting...")
        sys.exit()

    loghandler.print_log("Supply drop status success!")
    return response
