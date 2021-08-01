import os
from dotenv import load_dotenv
import requests
import json
import sys
import time
import schedule
import urllib.parse
from datetime import datetime
from rich.console import Console

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
    print('Retriving variables from .env file')
    WEBHALLEN_USERNAME = os.getenv('WEBHALLEN_USERNAME')
    WEBHALLEN_PASSWORD = os.getenv('WEBHALLEN_PASSWORD')
    VERBOSE = os.getenv('VERBOSE')
    print('Username:', WEBHALLEN_USERNAME if VERBOSE == 'True' else '*******')
    print('Password:', WEBHALLEN_PASSWORD if VERBOSE == 'True' else '*******')

    if WEBHALLEN_USERNAME == 'example_email' or WEBHALLEN_PASSWORD == 'example_password':
        print('Example username and password detected!')
        print('You need to change your .env file to continue...')
        sys.exit()
    print("\n")
    return WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD

# Sends request to login to webhallen
# Params: session
def login_request(session, WEBHALLEN_USERNAME: str, WEBHALLEN_PASSWORD: str):
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
    print('Sending supply drop status request...')
    response = session.get(
        url = SUPPLY_DROP_URL
    )

    if response.status_code != 200:
        print('Supply drop page failed. Exiting...')
        print('Status code:', response.status_code)
        sys.exit()
    else:
        print('Supply drop status success!')
    return response

# Sends request to collect weekly supply drop
# Params: Session after login success
# Params: Webhallen User ID
def weekly_supply_drop_request(session, WEBHALLEN_USER_ID: str):
    URL = 'https://www.webhallen.com/api/supply-drop'

    headers = {
        'referer': 'https://www.webhallen.com/se/member/'+str(WEBHALLEN_USER_ID)+'/supply-drop'
    }

    print('Sending request to grab weekly supply drop...')
    response = session.post(
        url=URL,
        headers=headers
    )

    if response.status_code == 403:
        print('Status code 403! No weekly supply drop to grab')
        return
    print(response)

# Sends request to collect activity supply drop
# Params: Session after login success
# Params: Webhallen User ID
def activity_supply_drop_request(session, WEBHALLEN_USER_ID: str):
    URL = 'https://www.webhallen.com/api/supply-drop'

    headers = {
        'authority': 'www.webhallen.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://www.webhallen.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.webhallen.com/se/member/'+str(WEBHALLEN_USER_ID)+'/supply-drop',
        'accept-language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    data = '{"crateType":"activity"}'

    print('Sending request to grab activity supply drop...')
    response = session.post(
        url=URL,
        headers=headers,
        data=data)

    if response.status_code == 403:
        print('Status code 403! No activity supply drop to grab')
        return
    print(response)

# EXPERIMENTAL, needs configuration!
# Sends request to collect level up supply drop
# Params: Session after login success
# Params: Webhallen User ID
def levelup_supply_drop_request(session, WEBHALLEN_USER_ID: str):
    URL = 'https://www.webhallen.com/api/supply-drop'

    headers = {
        'authority': 'www.webhallen.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://www.webhallen.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.webhallen.com/se/member/'+str(WEBHALLEN_USER_ID)+'/supply-drop',
        'accept-language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    data = '{"crateType":"level_up"}'

    print('Sending request to grab level up supply drop...')
    response = session.post(
        url=URL,
        headers=headers,
        data=data)

    if response.status_code == 403:
        print('Status code 403! No level up supply drop to grab')
        return
    print(response)

# Grabs users webhallen User ID
# Params: Session after login success
def grab_user_id(session):
    WEBHALLEN_USER_ID = os.getenv('WEBHALLEN_USER_ID')
    VERBOSE = os.getenv('VERBOSE')
    if WEBHALLEN_USER_ID == 'example_id':
        print('Webhallen User ID not set in .env file')
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
def supply_drop_status(response_supply_text):
    response_json = json.loads(response_supply_text)
    days, hours, minutes, seconds = get_drop_time(response_json['nextDropTime'])

    weekly_avaliable, activity_avaliable, levelup_avaliable = 0, 0, 0
    
    weekly_avaliable = int(response_json['crateTypes'][0]['openableCount'])
    activity_avaliable = int(response_json['crateTypes'][1]['openableCount'])
    levelup_avaliable = int(response_json['crateTypes'][2]['openableCount'])

    print('------ SUPPLY DROP STATUS ------')
    print(datetime.now().strftime('Time: %Y-%m-%d %H:%M:%S'))
    print('Weekly drop avaliable:', weekly_avaliable)
    if days + hours + minutes + seconds > 1:
        print(
        'Weekly drop time left:',
        (str(days) + " days") if days > 0 else '',
        (str(hours) + " hours") if hours > 0 else '',
        (str(minutes) + " minutes") if minutes > 0 else '',
        (str(seconds) + " seconds") if seconds > 0 else '')

    print('Activity drop avaliable:', activity_avaliable)
    print('Activity drop in: ' + str(response_json['crateTypes'][1]['nextResupplyIn']) + " drops")

    print('Level up drop avaliable:', levelup_avaliable)
    print('Level up drop progress: ' + str(response_json['crateTypes'][2]['progress'])[2:4] + "%")
    print('--------------------------------')

    return weekly_avaliable, activity_avaliable, levelup_avaliable


def main(WEBHALLEN_USERNAME: str, WEBHALLEN_PASSWORD: str):
    session = requests.Session()
    response_login = login_request(session, WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD)
    WEBHALLEN_USER_ID = grab_user_id(session)
    response_supply = supply_drop_request(session)
    weekly_avaliable, activity_avaliable, levelup_avaliable = supply_drop_status(response_supply.text)
    DEBUG = os.getenv('DEBUG')
    if DEBUG == 'True':
        weekly_supply_drop_request(session, WEBHALLEN_USER_ID)
        activity_supply_drop_request(session, WEBHALLEN_USER_ID)
        levelup_supply_drop_request(session, WEBHALLEN_USER_ID)
    else:
        if weekly_avaliable + activity_avaliable + levelup_avaliable >= 1:
            print('Supply drop avaliable.')
        
            for _ in range(weekly_avaliable):
                weekly_supply_drop_request(session, WEBHALLEN_USER_ID)
        
            for _ in range(activity_avaliable):
                activity_supply_drop_request(session, WEBHALLEN_USER_ID)
        
            for _ in range(levelup_avaliable):
                levelup_supply_drop_request(session, WEBHALLEN_USER_ID)
        else:
            print('No supply drop avaliable.')
    print('\n\n\n')


if __name__ == '__main__':
    print('AdiliusWSDG starting. \n')

    load_dotenv()
    console = Console()
    WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD = load_variables()
    CONTINUOUS = os.getenv('CONTINUOUS')

    if CONTINUOUS == 'True':
        main(WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD)
        schedule.every().day.at('00:10').do(main, WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD)
        with console.status(status='[bold green]Continuously running script....', spinner='material') as status:
            while 1:
                schedule.run_pending()
                time.sleep(1)
    else:
        main(WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD)
    
    print('AdiliusWSDG exiting!')
    sys.exit(1)