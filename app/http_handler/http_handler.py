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
        "referer": "https://www.webhallen.com/se/member/"
        + str(webhallen_user_id)
        + "/supply-drop"
    }

    logging.debug("Sending request to grab weekly supply drop...")
    response = session.post(url=SUPPLY_DROP_URL, headers=headers)

    # Handle no supply drop
    if response.status_code == 403:
        logging.debug(f"No weekly supply drop. Status code: {response.status_code}")
        return

    # Handle bad response
    if response.status_code != 200:
        logging.error(
            f"Error grabbing weekly supply drop. Status code: {response.status_code}"
        )
        return

    # Handle good response
    try:
        response_json = json.loads(response.text)
        for drop in response_json["drops"]:
            name = drop["name"]
            description = drop["description"]
            logging.info(f"Grabbed weekly drop {name} and got {description}")
    except:
        logging.info(
            f"Grabbed weekly drop. But failed to parse response text. Saving response for debugging"
        )
        logging.info(response)
        logging.info(response.text)


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

    # Handle no activity drop
    if response.status_code == 403:
        logging.debug(f"No activity supply drop. Status code: {response.status_code}")
        return response

    # Handle bad response
    if response.status_code != 200:
        logging.error(
            f"Error grabbing activity supply drop. Status code: {response.status_code}"
        )
        return response

    # Handle good response
    try:
        response_json = json.loads(response.text)
        for drop in response_json["drops"]:
            name = drop["name"]
            description = drop["description"]
            logging.info(f"Grabbed activity drop {name} and got {description}")
    except:
        logging.info(
            f"Grabbed activity drop. But failed to parse response text. Saving response for debugging"
        )
        logging.info(response)
        logging.info(response.text)


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

    logging.debug("Sending request to grab level up supply drop...")
    response = session.post(url=url, headers=headers, data=data)

    # Handle no activity drop
    if response.status_code == 403:
        logging.debug(f"No level up supply drop. Status code: {response.status_code}")
        return response

    # Handle bad response
    if response.status_code != 200:
        logging.error(
            f"Error grabbing level up supply drop. Status code: {response.status_code}"
        )
        return

    # Handle good response
    try:
        # Response parsing success
        response_json = json.loads(response.text)
        for drop in response_json["drops"]:
            name = drop["name"]
            description = drop["description"]
            logging.info(f"Grabbed level up drop {name} and got {description}")
    except:
        # Response parsing failed
        logging.info(
            f"Grabbed level up drop. But failed to parse response text. Saving response for debugging"
        )
        logging.info(response)
        logging.info(response.text)
