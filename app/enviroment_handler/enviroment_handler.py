"""
Module to handle enviroment variables in the program
Prompting user, encrypting to file, and reading from file
"""

import os
import uuid
import json
import getpass

# Handles enviroment variables
class EnvHandler:
    """
    Class to handle enviroment variables
    """

    def __init__(self):
        self.root_path = os.getcwd()
        self.path_to_data = "app/data/"
        self.env_file = ".env"
        self.path_to_list = "app/enviroment_handler/"
        self.enviroment_variables_list = ".enviroment_variables"
        self.variables = {}
        self.key = str(uuid.getnode())  # Get hardware adress as 48-bit positive integer
        self.init()

    def init(self):
        """
        Initialize enviroment handler class

        """
        if self.is_env_file_presence():
            try:
                self.read_env_contents()
            except FileNotFoundError:
                print("Error reading enviroment file")
                self.prompt_new_env()
        else:
            self.prompt_new_env()

    # Checks if .env file exists
    def is_env_file_presence(self):
        """
        Returns true if enviroment variable file exists
        """

        if os.path.isfile(os.path.join(self.root_path, self.env_file)):
            return True
        return False

    # Returns list of variable names and descriptions
    def getenviroment_variables_list(self):
        """
        Returns list of enviroment variables names
        Returns list of enviroment variables description
        """

        # List to hold variable names
        enviroment_variables_names = []

        # List to hold variable descriptions
        enviroment_variables_description = []

        # Open file and read contents
        with open(
            file=os.path.join(
                self.root_path,
                "app/enviroment_handler/",
                self.enviroment_variables_list,
            ),
            mode="r",
            encoding="utf-8",
        ) as env_file:
            for line in env_file.read().splitlines():
                name, description = line.split(",")
                enviroment_variables_names.append(name)
                enviroment_variables_description.append(description)

        return enviroment_variables_names, enviroment_variables_description

    def encode(self, plaintext):
        """
        Returns encoded ciphertext using initialized key
        """
        encoded_chars = []

        for index, character in enumerate(plaintext):
            key_c = self.key[index % len(self.key)]
            encoded_c = chr(ord(character) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        ciphertext = "".join(encoded_chars)
        return ciphertext

    def decode(self, ciphertext):
        """
        Returns decoded plaintext using initialized key
        """

        decoded_chars = []
        for index, character in enumerate(ciphertext):
            key_c = self.key[index % len(self.key)]
            decoded_c = chr((ord(character) - ord(key_c) + 256) % 256)
            decoded_chars.append(decoded_c)
        plaintext = "".join(decoded_chars)
        return plaintext

    def read_env_contents(self):
        """
        Returns enviroment variables contents as dictionary
        """

        if self.is_env_file_presence():

            # Open .env file
            with open(
                file=os.path.join(self.root_path, self.env_file),
                mode="r",
                encoding="utf-8",
            ) as env_file:

                # Read ciphertext contents
                ciphertext = env_file.read()

                # Close .env file
                env_file.close()

                # Decipher to plaintext
                plaintext = self.decode(ciphertext)

                # Save enviroment variables to class
                self.variables = json.loads(plaintext)

    def write_env_contents(self):
        """
        Write enviroment variables to .env file
        """

        # Enviroment variables to json string
        json_env = json.dumps(self.variables)

        # Create file
        with open(
            os.path.join(self.root_path, self.env_file), "w", encoding="utf-8"
        ) as env_file:
            # Encode to ciphertext
            ciphertext = self.encode(json_env)

            # Write ciphertext to .env
            env_file.write(ciphertext)

            # Close .env file
            env_file.close()

    def prompt_new_env(self):
        """
        Prompt user to enter new enviroment variables
        """

        # Get enivorment variables to prompt user
        names, descriptions = self.getenviroment_variables_list()

        # Clear old variables
        print("Setting new enviroment variables...")
        self.variables.clear()

        # Ask user for variables
        for name, description in zip(names, descriptions):
            if name == "WEBHALLEN_PASSWORD":
                variable = getpass.getpass(prompt=(description + ": "))
            else:
                variable = input(description + ": ")
            self.variables[name] = variable

        if self.get_variable("SAVE_ENV") == "y":
            self.write_env_contents()

    def get_variable(self, variable_name):
        """
        Returns value of variable
        """
        return self.variables[variable_name]
