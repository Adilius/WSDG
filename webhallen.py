import os
from dotenv import load_dotenv
import requests
import json
import sys
import time
import re

print('AdiliusWSDG starting.')

def get_drop_time(airplane_time: float):
    current_time = round(time.time())
    time_difference = airplane_time - current_time
    days = time_difference // 86400
    hours = (time_difference - days*86400) // 3600
    minutes = (time_difference - days*86400 - hours*3600) // 60
    seconds = (time_difference - days*86400 - hours*3600 - minutes*60)
    return days, hours, minutes, seconds

print('Retriving variables from .env file...')
load_dotenv()
WEBHALLEN_USERNAME = os.getenv('WEBHALLEN_USERNAME')
WEBHALLEN_PASSWORD = os.getenv('WEBHALLEN_PASSWORD')
print('Username:',WEBHALLEN_USERNAME)
print('Password:', WEBHALLEN_PASSWORD)

if WEBHALLEN_USERNAME == 'example_email' or WEBHALLEN_PASSWORD == 'example_password':
    print('Example username and password detected!')
    print('You need to change your .env file to continue...')
    sys.exit()

LOGIN_URL = "https://www.webhallen.com/api/login"
SUPPLY_DROP_URL = 'https://www.webhallen.com/api/supply-drop'

HEADERS = {
    'Content-Type': 'application/json'
}

BODY = json.dumps({
    'username':WEBHALLEN_USERNAME,
    'password':WEBHALLEN_PASSWORD
})

session = requests.Session()

print('Making login request...')
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

for cookie in session.cookies:
    user_id = re.search(r'%\d?\D([0-9]+)',cookie.value)
    print("User ID:", user_id)
    break

print('Supply drop page request...')
response = session.get(
    url = SUPPLY_DROP_URL
)

if response.status_code != 200:
    print('Supply drop page failed. Exiting...')
    print('Status code:', response.status_code)
    sys.exit()
else:
    print('Supply drop page success!')
    print('-----------------------------------')

response_text = json.loads(response.text)
days, hours, minutes, seconds = get_drop_time(response_text['nextDropTime'])
print('Supply drop avaliable:', 'True' if response_text['crateTypes'][0]['openableCount'] > 0 else 'False')
print(
    'Supply drop time left:',
    (str(days) + " days") if days > 0 else '',
    (str(hours) + " hours") if hours > 0 else '',
    (str(minutes) + " minutes") if minutes > 0 else '',
    (str(seconds) + " seconds") if seconds > 0 else '')

print('Activity drop avaliable:', 'True' if response_text['crateTypes'][1]['openableCount'] > 0 else 'False')
print('Activity drop in: ' + str(response_text['crateTypes'][1]['nextResupplyIn']) + " drops")

print('Level up drop avaliable:', 'True' if response_text['crateTypes'][2]['openableCount'] > 0 else 'False')
print('Level up drop progress: ' + str(response_text['crateTypes'][2]['progress'])[2:4] + "%")
