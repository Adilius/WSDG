"""
Module to handle all HTTP requests sent to Webhallen
"""
import json
import sys
import logging

API_BASE_URL = "https://www.webhallen.com/api/"
LOGIN_URL = "https://www.webhallen.com/api/login/"
SUPPLY_DROP_URL = "https://www.webhallen.com/api/supply-drop/"


def login_request(session, webhallen_username: str, webhallen_password: str):
    """
    Sends request to login to webhallen
    Params: A new requests session
    Returns: Response
    """

    headers = {"Content-Type": "application/json"}
    body = json.dumps({"username": webhallen_username, "password": webhallen_password})
    logging.debug("Sending login request...")
    logging.debugv("Webhallen username: " + webhallen_username)
    logging.debugv("Webhallen password: " + webhallen_password)

    response = session.post(url=LOGIN_URL, headers=headers, data=body)
    if response.status_code == 403:
        logging.critical(f"Login failed. Status code: {response.status_code}")
        logging.critical(
            f"Possibly wrongly set username and password. Exiting program..."
        )
        sys.exit()

    if response.status_code != 200:
        logging.critical(f"Login critical fail. Status code: {response.status_code}")
        logging.critical(f"Exiting program....")
        sys.exit()

    # Response code 200
    logging.debug("Login success!")
    return response


def supply_drop_request(session):
    """
    Sends request to webhallen supply drop status API
    Params: A new requests session
    Returns: Response
    """
    logging.debug("Sending supply drop status request...")
    response = session.get(url=SUPPLY_DROP_URL)

    if response.status_code != 200:
        logging.warning(f"Supply drop status failed: {response.status_code}")
        logging.warning(f"Will continue program anyways...")
        return False, response

    # Response code 200
    logging.debug("Supply drop status success!")
    return True, response


def weekly_supply_drop_request(session, webhallen_user_id: str):
    """
    Params: Session after login success
    Params: Webhallen User ID
    Sends request to collect weekly supply drop
    """
    headers = {
        "referer": "https://www.webhallen.com/se/member/" + str(webhallen_user_id) + "/supply-drop"
    }

    logging.debug("Sending request to grab weekly supply drop...")
    response = session.post(url=SUPPLY_DROP_URL, headers=headers)

    log_handle_response(response, "weekly")
    return response


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
    logging.debug("Sending request to grab activity supply drop...")
    response = session.post(url=url, headers=headers, data=data)

    log_handle_response(response, "activity")
    return response


def levelup_supply_drop_request(session, webhallen_user_id: str):
    """
    Working state, HTTP parameters needs configuration!
    Params: Session after login success
    Params: Webhallen User ID
    Sends request to collect level up supply drop
    """

    url = "https://www.webhallen.com/api/supply-drop"
    headers = {
        "authority": "www.webhallen.com",
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',    # Possibly redundant
        "origin": "https://www.webhallen.com",
        'dnt': '1',                                                                         # Possibly redundant
        'sec-ch-ua-mobile': '?0',                                                           # Possibly redundant
        'sec-fetch-site': 'same-origin',                                                    # Possibly redundant
        'sec-fetch-mode': 'cors',                                                           # Possibly redundant
        'sec-fetch-dest': 'empty',                                                          # Possibly redundant
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',    # Possibly neccesary
        'content-type': 'application/json',                                                                                                     # Possibly neccesary
        'accept': '*/*',                                                                                                                        # Possibly neccesary
        "referer": "https://www.webhallen.com/se/member/" + str(webhallen_user_id) + "/supply-drop",
    }
    data = '{"crateType":"level-up"}'

    logging.debug("Sending request to grab level up supply drop...")
    response = session.post(url=url, headers=headers, data=data)

    log_handle_response(response, "level up")
    return response

def log_handle_response(response, supply_drop_type: str):
    """
    Params: Response object
    Params: Supply drop type
    Logs response according to status code and supply drop type
    """

    # Handle no supply drop
    if response.status_code == 403:
        logging.debug(f"No {supply_drop_type} supply drop. Status code: {response.status_code}")
        return response

    # Handle bad response
    if response.status_code != 200:
        logging.error(f"Error grabbing {supply_drop_type} supply drop. Status code: {response.status_code}")
        return response

    # Handle good response
    try:
        # Response parsing success
        response_json = json.loads(response.text)
        for drop in response_json["drops"]:
            name = drop["name"]
            description = drop["description"]
            logging.info(f"Grabbed {supply_drop_type} supply drop {name}{' ' if description == '' else f' and got {description}'}")
    except:
        # Response parsing failed
        logging.info(f"Grabbed {supply_drop_type} supply drop. But failed to parse response text. Logging response for debugging")
        logging.info(response)
        logging.info(response.text)
    return response