"""
Module to handle enviroment variables in the program
Prompting user, encrypting to file, and reading from file
"""

import os
import uuid
import json
import re
import logging
from pathlib import Path

# Handles enviroment variables
class EnvHandler:
    """
    Class to handle enviroment variables
    """
    def __init__(self, email: str, password: str, store: bool):
        logging.debug("Initialising enviroment handler...")

        # Get path to root folder
        self.root_path = Path(__file__).parents[2]

        # Store variables
        self.variables = {}
        self.key = str(uuid.getnode())      # Get hardware adress as 48-bit positive integer

        # Create enviroment file
        self.init(email, password, store)

    def init(self, email, password, store):
        """
        Initialize enviroment handler class
        """

        # Validate command-line argument variables
        if isinstance(email, str) and re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            logging.debug("Email argument valid.")
            logging.debugv(f"Setting new email: {email}")
            self.variables["email"] = email
        else:
            logging.debug("Email argument invalid.")
            #logging.debugv(f"Retriving stored email: {self.variables['email']}")

        
        if isinstance(password, str) and len(password) >= 8:
            logging.debug("Password argument valid.")
            logging.debugv(f"Setting new password: {password}")
            self.variables["password"] = password
        else:
            logging.debug("Password argument invalid.")
            #logging.debugv(f"Retriving stored password: {self.variables['password']}")

        # Try to read enviroment file
        if self.is_enviroment_file_present():
            try:
                self.read_env_contents()
            except FileNotFoundError:
                logging.debug("Could not find enviroment file.")

        # Store email and password
        if store:
            logging.debug("Writing enviroment variables.")
            self.write_enviroment_variables()

    def is_enviroment_file_present(self):
        """
        Returns true if enviroment variable file exists
        """
        relative_env_file_path = os.path.join(self.root_path, ".env")
        if os.path.isfile(relative_env_file_path):
            return True
        return False

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
        if self.is_enviroment_file_present():

            # Open .env file
            with open(
                file=os.path.join(self.root_path, ".env"),
                mode="r",
                encoding="utf-8",
            ) as env_file_name:

                ciphertext = env_file_name.read()       # Read ciphertext from .env
                plaintext = self.decode(ciphertext)     # Encode to ciphertext

                # Save enviroment variables to class
                try:
                    self.variables = json.loads(plaintext)
                except:
                    logging.debug("Failed to parse enviroment file!")

    def write_enviroment_variables(self):
        """
        Write enviroment variables to .env file
        """
        # Enviroment variables to json string
        json_env = json.dumps(self.variables)

        # Create file
        with open(
            os.path.join(self.root_path, ".env"), "w", encoding="utf-8"
        ) as env_file_name:
            
            ciphertext = self.encode(json_env)  # Encode to ciphertext
            env_file_name.write(ciphertext)     # Write ciphertext to .env

    def get_variable(self, variable_name):
        """
        Returns value of variable
        """
        return self.variables[variable_name]
