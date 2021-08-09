import os
import sys
from dotenv import load_dotenv

# Handles enviroment variables
class envhandler():

    def __init__(self):
        self.path_to_root = "../"
        self.env = ".env"
        self.enviromentVariablesList = '.enviroment_variables'

    def checkFilePresence(self):

        # If .env file exists
        if os.path.isfile(self.path_to_root + self.env):
            return True
        return False

    def getEnviromentVariablesList(self):

        # List to hold variable names
        enviromentVariablesNames = []

        # List to hold variable descriptions
        enviromentVariablesDescription = []

        # Open file and read contents
        with open(self.enviromentVariablesList) as env_file:
            for line in env_file:
                name, description = line.split(',')
                enviromentVariablesNames.append(name)
                enviromentVariablesDescription.append(description)

        return enviromentVariablesNames, enviromentVariablesDescription


    def checkFileContents(self):

        # If .env file exists
        if self.checkFilePresence() == True:
            load_dotenv(dotenv_path=self.path_to_root)
            enviroment_variable_list = []
            with open

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
        sys.exit(1)
    print()
    return WEBHALLEN_USERNAME, WEBHALLEN_PASSWORD

# Grabs users webhallen User ID
# Params: Session after login success
def grab_user_id(session):
    WEBHALLEN_USER_ID = os.getenv('WEBHALLEN_USER_ID')
    VERBOSE = os.getenv('VERBOSE')
    if WEBHALLEN_USER_ID == 'example_id':
        print('Webhallen User ID not set in .env file')
    elif len(WEBHALLEN_USER_ID) <= 4 or len(WEBHALLEN_USER_ID) >= 10 or not WEBHALLEN_USER_ID.isdigit():
        print('Wrongly set User ID in env.')
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

    os.environ['WEBHALLEN_USER_ID'] = str(WEBHALLEN_USER_ID)
    print()
    return WEBHALLEN_USER_ID