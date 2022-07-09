"""
Module to handle enviroment variables in the program
Prompting user, encrypting to file, and reading from file
"""

import os
import uuid
import json
import getpass
import sys

from pathlib import Path

from ..logging_handler import logging_handler

# Handles enviroment variables
class EnvHandler:
    """
    Class to handle enviroment variables
    """

    def __init__(self):
        # Get paths
        self.module_path = Path(__file__).parents[0]
        self.root_path = Path(__file__).parents[2]

        # Enviroment file names
        self.enviroment_variables_name = ".enviroment_variables"

        # Store variables
        self.variables = {}
        self.key = str(uuid.getnode())  # Get hardware adress as 48-bit positive integer

        # Get or Create enviroment file
        self.init()


    def init(self):
        """
        Initialize enviroment handler class

        """
        if self.is_env_file_presence():
            try:
                self.read_env_contents()
            except FileNotFoundError:
                print("Could not find enviroment file. Creating new...")
                self.prompt_new_env()
        else:
            self.prompt_new_env()

    # Checks if .env file exists
    def is_env_file_presence(self):
        """
        Returns true if enviroment variable file exists
        """
        relative_env_file_path = os.path.join(self.root_path, ".env")
        if os.path.isfile(relative_env_file_path):
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
                self.module_path,
                self.enviroment_variables_name
            ),
            mode="r",
            encoding="utf-8",
        ) as env_file_name:
            for line in env_file_name.read().splitlines():
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
                file=os.path.join(self.root_path, ".env"),
                mode="r",
                encoding="utf-8",
            ) as env_file_name:

                # Read ciphertext contents
                ciphertext = env_file_name.read()

                # Close .env file
                env_file_name.close()

                # Decipher to plaintext
                plaintext = self.decode(ciphertext)

                # Save enviroment variables to class
                try:
                    self.variables = json.loads(plaintext)
                except:
                    loghandler = logging_handler.LogHandler()
                    loghandler.print_log("Failed to read enviroment file! Try deleting file and re-create it. Exiting program...")
                    sys.exit(1)

    def write_env_contents(self):
        """
        Write enviroment variables to .env file
        """

        # Enviroment variables to json string
        json_env = json.dumps(self.variables)

        # Create file
        with open(
            os.path.join(self.root_path, ".env"), "w", encoding="utf-8"
        ) as env_file_name:
            # Encode to ciphertext
            ciphertext = self.encode(json_env)

            # Write ciphertext to .env
            env_file_name.write(ciphertext)

            # Close .env file
            env_file_name.close()

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
