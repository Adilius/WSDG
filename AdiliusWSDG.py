import requests
import json
import sys
import time
import schedule
import urllib.parse
from datetime import datetime
from rich.console import Console
from app.enviroment_handler import enviroment_handler
from app.logging_handler import logging_handler
from app.http_handler import http_handler

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


    # Handle bad response
    if response.status_code != 200:
        error_msg = f'Error grabbing weekly supply drop. Status code: {response.status_code}'
        print(error_msg)
        loghandler.print_log(error_msg)
        return

    response_json = json.loads(response.text)
    for drop in response_json['drops']:
        name = drop['name']
        description = drop['description']
        loghandler.print_log(f'Grabbed supply drop {name} and got {description}')

# Sends request to collect activity supply drop
# Params: Session after login success
# Params: Webhallen User ID
def activity_supply_drop_request(session, WEBHALLEN_USER_ID: str):
    URL = 'https://www.webhallen.com/api/supply-drop'

    headers = {
        'authority': 'www.webhallen.com',
        'origin': 'https://www.webhallen.com',
        'referer': 'https://www.webhallen.com/se/member/'+str(WEBHALLEN_USER_ID)+'/supply-drop',
    }

    data = '{"crateType":"activity"}'

    print('Sending request to grab activity supply drop...')
    response = session.post(
        url=URL,
        headers=headers,
        data=data)

    # Handle bad response
    if response.status_code != 200:
        error_msg = f'Error grabbing activity supply drop. Status code: {response.status_code}'
        print(error_msg)
        loghandler.print_log(error_msg)
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
    'origin': 'https://www.webhallen.com',
    'referer': 'https://www.webhallen.com/se/member/'+str(WEBHALLEN_USER_ID)+'/supply-drop',
    }

    data = '{"crateType":"level-up"}'

    print('Sending request to grab level up supply drop...')
    response = session.post(
        url=URL,
        headers=headers,
        data=data)

    # Handle bad response
    if response.status_code != 200:
        error_msg = f'Error grabbing level up supply drop. Status code: {response.status_code}'
        print(error_msg)
        loghandler.print_log(error_msg)
        return

    print(response)

# Grabs users webhallen User ID
# Params: Session after login success
def grab_user_id(session):

    VERBOSE = envHandler.getVariable('VERBOSE')
    loghandler.print_log('Grabbing Webhallen User ID from cookies')
    try:
        webhallen_auth_cookie = session.cookies['webhallen_auth']
        WEBHALLEN_USER_ID = json.loads(urllib.parse.unquote(webhallen_auth_cookie))
    except:
        loghandler.print_log('Failure! Exiting program')
        sys.exit(1)
    else:
        loghandler.print_log('Webhallen User ID: ' + WEBHALLEN_USER_ID['user_id'] if VERBOSE == 'y' else 'Webhallen User ID: *******')

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
    response_login = http_handler.login_request(session, WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD)
    WEBHALLEN_USER_ID = grab_user_id(session)
    response_supply = http_handler.supply_drop_request(session)
    weekly_avaliable, activity_avaliable, levelup_avaliable = supply_drop_status(response_supply.text)
    if weekly_avaliable + activity_avaliable + levelup_avaliable >= 1:
        print('Supply drop avaliable.')
        
        for _ in range(weekly_avaliable):
            weekly_supply_drop_request(session, WEBHALLEN_USER_ID)
        
        for _ in range(activity_avaliable):
            activity_supply_drop_request(session, WEBHALLEN_USER_ID)
        
        for _ in range(levelup_avaliable):
            levelup_supply_drop_request(session, WEBHALLEN_USER_ID)
    else:
        loghandler.print_log('No supply drop avaliable.')

if __name__ == '__main__':

    # Start logging handler
    loghandler = logging_handler.loghandler()
    loghandler.print_log('AdiliusWSDG starting.')

    # Get enviroment variables
    envHandler = enviroment_handler.envhandler()
    WEBHALLEN_USERNAME = envHandler.getVariable('WEBHALLEN_USERNAME')
    WEBHALLEN_PASSWORD = envHandler.getVariable('WEBHALLEN_PASSWORD')
    CONTINUOUS = envHandler.getVariable('CONTINUOUS')

    # Continiously running the program
    if CONTINUOUS == 'y':

        # Run once first
        main(WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD)

        # Schedule running
        schedule.every().day.at('17:54').do(main, WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD)

        print(f'Continuously running script....')
        while 1:
            schedule.run_pending()
            time.sleep(1)

    # Run one time
    else:
        main(WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD)
    
        loghandler.print_log('AdiliusWSDG exiting.')
        sys.exit(1)