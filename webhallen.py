import os
from dotenv import load_dotenv
import requests
import json
import sys
import time
import re
import urllib.parse

print('AdiliusWSDG starting.')

# Params: Weekly Supply Drop epoch time
# Returns: days, hours, minutes, seconds until next drop
def get_drop_time(airplane_time: float):
    current_time = round(time.time())
    time_difference = int(airplane_time - current_time)
    days = time_difference // 86400
    hours = (time_difference - days*86400) // 3600
    minutes = (time_difference - days*86400 - hours*3600) // 60
    seconds = (time_difference - days*86400 - hours*3600 - minutes*60)
    return days, hours, minutes, seconds

# Loads username and password from .env
def load_variables():
    print('Retriving variables from .env file...')
    load_dotenv()
    WEBHALLEN_USERNAME = os.getenv('WEBHALLEN_USERNAME')
    WEBHALLEN_PASSWORD = os.getenv('WEBHALLEN_PASSWORD')
    VERBOSE = os.getenv('VERBOSE')
    print('Username:', WEBHALLEN_USERNAME if VERBOSE == 'True' else '*******')
    print('Password:', WEBHALLEN_PASSWORD if VERBOSE == 'True' else '*******')

    if WEBHALLEN_USERNAME == 'example_email' or WEBHALLEN_PASSWORD == 'example_password':
        print('Example username and password detected!')
        print('You need to change your .env file to continue...')
        sys.exit()
    return WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD

# Sends request to login to webhallen
# Params: session
def login_request(session):
    LOGIN_URL = "https://www.webhallen.com/api/login"
    HEADERS = {
        'Content-Type': 'application/json'
    }
    BODY = json.dumps({
        'username':WEBHALLEN_USERNAME,
        'password':WEBHALLEN_PASSWORD
    })
    print('Sending login request...')
    response = session.post(
        url=LOGIN_URL,
        headers=HEADERS,
        data=BODY
    )
    if response.status_code == 403:
        print('Forbidden access')
        print('Possibly wrongly set username and password')
        print('Exiting...')
        sys.exit()
    elif response.status_code != 200:
        print('Status code:', response.status_code)
        print('Login failed. Exiting...')
        sys.exit()
    else:
        print('Login success!')
        return response

# Sends status request to webhallen supply drop API
# Params: Session after login success
def supply_drop_request(session):
    SUPPLY_DROP_URL = 'https://www.webhallen.com/api/supply-drop'
    print('Sending supply drop page request...')
    response = session.get(
        url = SUPPLY_DROP_URL
    )

    if response.status_code != 200:
        print('Supply drop page failed. Exiting...')
        print('Status code:', response.status_code)
        sys.exit()
    else:
        print('Supply drop page success!')
    return response

# Sends request to collect weekly supply drop
# Params: Session after login success
def weekly_supply_drop_request(session):
    URL = 'https://www.webhallen.com/api/supply-drop'

    headers = {
        'authority': 'www.webhallen.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'accept': '*/*',
        'origin': 'https://www.webhallen.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.webhallen.com/se/member/2476589/supply-drop',
        'accept-language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
        'if-none-match': 'W/"baba8c477accc6360515317229897469"',
        'content-length': '0',
        'region': 'se',
        'cookie': 'ref=www.google.com; last_visit=1626944502; webhallen_auth=%7B%22user_id%22%3A2476589%2C%22token%22%3A%22VBVMO8uoDoQKZt7VspQLql3t2ugNLdo3Ls78IzGdZYA%3D%22%7D; webhallen=muHHAnQr0m7x0m8SMzRSxw309awlNuyjyLCBsWSI',
        'Referer': 'https://cdn.webhallen.com/css/app.1308.css',
        'DNT': '1'
    }
    response = session.post(
        url=URL
    )

# Grabs users webhallen User ID
# Params: Session after login success
def grab_user_id(session):
    WEBHALLEN_USER_ID = os.getenv('WEBHALLEN_USER_ID')
    VERBOSE = os.getenv('VERBOSE')
    if WEBHALLEN_USER_ID == 'example_id':
        print('Webhallen User ID not set. Grabbing User ID from cookies')
    elif len(WEBHALLEN_USER_ID) <= 4 or len(WEBHALLEN_USER_ID) >= 10 or not WEBHALLEN_USER_ID.isdigit():
        print('Wrongly set User ID. Grabbing User ID from cookies')
    else:
        print('User ID retrived from .env file:', WEBHALLEN_USER_ID)
        return WEBHALLEN_USER_ID

    print('Grabbing Webhallen User ID from cookies')
    try:
        webhallen_auth_cookie = session.cookies['webhallen_auth']
        WEBHALLEN_USER_ID = json.loads(urllib.parse.unquote(webhallen_auth_cookie))
        print('Success! Webhallen User ID:', WEBHALLEN_USER_ID['user_id'] if VERBOSE == 'True' else '*******')
    except:
        print('Failure! Exiting program')
        sys.exit(1)

    return WEBHALLEN_USER_ID

# Prints all supply drop status
# Params: Response from supply drop request
def print_supply_drop_status(response_supply_text):
    response_json = json.loads(response_supply_text)
    days, hours, minutes, seconds = get_drop_time(response_json['nextDropTime'])
    print('------ SUPPLY DROP STATUS ------')
    print('Supply drop avaliable:', 'True' if response_json['crateTypes'][0]['openableCount'] > 0 else 'False')
    if days + hours + minutes + seconds > 1:
        print(
        'Supply drop time left:',
        (str(days) + " days") if days > 0 else '',
        (str(hours) + " hours") if hours > 0 else '',
        (str(minutes) + " minutes") if minutes > 0 else '',
        (str(seconds) + " seconds") if seconds > 0 else '')

    print('Activity drop avaliable:', 'True' if response_json['crateTypes'][1]['openableCount'] > 0 else 'False')
    print('Activity drop in: ' + str(response_json['crateTypes'][1]['nextResupplyIn']) + " drops")

    print('Level up drop avaliable:', 'True' if response_json['crateTypes'][2]['openableCount'] > 0 else 'False')
    print('Level up drop progress: ' + str(response_json['crateTypes'][2]['progress'])[2:4] + "%")
    print('--------------------------------')

WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD = load_variables()
session = requests.Session()
response_login = login_request(session)
WEBHALLEN_USER_ID = grab_user_id(session)
response_supply = supply_drop_request(session)
print_supply_drop_status(response_supply.text)


