import os
import uuid
import json
import getpass

# Handles enviroment variables
class envhandler():

    def __init__(self):
        self.path_to_data = "AdiliusWSDG/data/"
        self.env = ".env"
        self.path_to_list = "AdiliusWSDG/enviroment_handler/"
        self.enviromentVariablesList = '.enviroment_variables'
        self.variables = {}
        self.key = str(uuid.getnode())  # Get hardware adress as 48-bit positive integer
        self.init()

    def init(self):
        if self.checkEnvFilePresence():
            try:
                self.readEnvContents()
            except:
                print('Error reading enviroment file')
                self.promptNewEnv()
                if self.getVariable('SAVE_ENV') == 'y':
                    self.writeEnvContents()
        else:
            self.promptNewEnv()
            if self.getVariable('SAVE_ENV') == 'y':
                self.writeEnvContents()

    # Checks if .env file exists
    def checkEnvFilePresence(self):

        if os.path.isfile(self.path_to_data + self.env):
            return True
        return False

    # Returns list of variable names and descriptions
    def getEnviromentVariablesList(self):

        # List to hold variable names
        enviromentVariablesNames = []

        # List to hold variable descriptions
        enviromentVariablesDescription = []

        # Open file and read contents
        with open(self.path_to_list + self.enviromentVariablesList) as env_file:
            for line in env_file.read().splitlines():
                name, description = line.split(',')
                enviromentVariablesNames.append(name)
                enviromentVariablesDescription.append(description)

        return enviromentVariablesNames, enviromentVariablesDescription

    #Encodes string using key
    def encode(self, string):
        encoded_chars = []

        for i in range(len(string)):
            key_c = self.key[i % len(self.key)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = "".join(encoded_chars)
        return encoded_string

    #Decodes string using key
    def decode(self, string):
        encoded_chars = []
        
        encoded_chars = []
        for i in range(len(string)):
            key_c = self.key[i % len(self.key)]
            encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = ''.join(encoded_chars)
        return encoded_string

    # Read .env to env list
    def readEnvContents(self):

        # If .env file exists
        if self.checkEnvFilePresence() == True:

            # Open .env file
            env_file = open(self.path_to_data + self.env, 'r', encoding='utf-8')

            # Read ciphertext contents
            ciphertext = env_file.read()

            # Close .env file
            env_file.close()

            # Decipher to plaintext
            plaintext = self.decode(ciphertext)

            # Save enviroment variables to class
            self.variables = json.loads(plaintext)
            
    # Write env list to .ev
    def writeEnvContents(self):

        # Enviroment variables to json string
        json_env = json.dumps(self.variables)

        # Open .env file for writing
        env_file = open(self.path_to_data + self.env, 'w', encoding='utf-8')  # open file for writing

        # Encode to ciphertext
        ciphertext = self.encode(json_env)

        # Write ciphertext to .env
        env_file.write(ciphertext)

        # Close .env file
        env_file.close()

    # Get new enviroment variables from user
    def promptNewEnv(self):

        # Get enivorment variables to prompt user
        names, descriptions = self.getEnviromentVariablesList()
        
        # Clear old variables
        print('Setting new enviroment variables...')
        self.variables.clear()

        # Ask user for variables
        for i in range(len(names)):
            if names[i] == 'WEBHALLEN_PASSWORD':
                variable = getpass.getpass(prompt=(descriptions[i]+": "))
            else:
                variable = input(descriptions[i] + ": ")
            self.variables[names[i]] = variable

    # Returns variable value given variable name
    def getVariable(self, variable_name):
        return self.variables[variable_name]