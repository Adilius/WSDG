from ..logging_handler import logging_handler
from ..enviroment_handler import enviroment_handler
import json, sys

# Sends request to login to webhallen
# Params: session
def login_request(session, WEBHALLEN_USERNAME: str, WEBHALLEN_PASSWORD: str):
    loghandler = logging_handler.loghandler()
    envHandler = enviroment_handler.envhandler()
    VERBOSE = envHandler.getVariable("VERBOSE")

    LOGIN_URL = "https://www.webhallen.com/api/login"
    HEADERS = {"Content-Type": "application/json"}
    BODY = json.dumps({"username": WEBHALLEN_USERNAME, "password": WEBHALLEN_PASSWORD})
    loghandler.print_log("Sending login request...")
    loghandler.print_log(
        "Webhallen username: " + WEBHALLEN_USERNAME
        if VERBOSE == "y"
        else "Webhallen username: *******"
    )
    loghandler.print_log(
        "Webhallen password: " + WEBHALLEN_PASSWORD
        if VERBOSE == "y"
        else "Webhallen password: *******"
    )

    response = session.post(url=LOGIN_URL, headers=HEADERS, data=BODY)
    if response.status_code == 403:
        loghandler.print_log("Forbidden access: Status code 403")
        loghandler.print_log("Possibly wrongly set username and password")
        loghandler.print_log("Exiting...")
        sys.exit()
    elif response.status_code != 200:
        loghandler.print_log("Status code:", response.status_code)
        loghandler.print_log("Login failed. Exiting...")
        sys.exit()

    loghandler.print_log("Login success!")
    return response


# Sends status request to webhallen supply drop API
# Params: Session after login success
def supply_drop_request(session):
    loghandler = logging_handler.loghandler()
    SUPPLY_DROP_URL = "https://www.webhallen.com/api/supply-drop"
    loghandler.print_log("Sending supply drop status request...")
    response = session.get(url=SUPPLY_DROP_URL)

    if response.status_code != 200:
        loghandler.print_log("Status code:", response.status_code)
        loghandler.print_log("Supply drop page failed. Exiting...")
        sys.exit()

    loghandler.print_log("Supply drop status success!")
    return response
