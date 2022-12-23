"""
Module to handle enviroment variables to and from file.
File contains an encoded JSON text with the format
{
    "email": some_email,
    "password": some_password    
}
"""

import os
import uuid
import json
import re
import logging
from pathlib import Path

root_path = Path(__file__).parents[2]

def get_env():
    if not is_enviroment_file_present():
        return None, None

    email, password = read_env_contents()
    return email, password

def set_env(email, password):
    if not is_enviroment_file_present():


def is_enviroment_file_present():
    """
    Returns true if enviroment variable file exists
    """
    relative_env_file_path = os.path.join(root_path, ".env")
    if os.path.isfile(relative_env_file_path):
        return True
    return False

def encode(key, plaintext):
    """
    Returns encoded ciphertext using initialized key
    """
    encoded_chars = []
    for index, character in enumerate(plaintext):
        key_c = key[index % len(key)]
        encoded_c = chr(ord(character) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    ciphertext = "".join(encoded_chars)
    return ciphertext
def decode(key, ciphertext):
    """
    Returns decoded plaintext using initialized key
    """
    decoded_chars = []
    for index, character in enumerate(ciphertext):
        key_c = key[index % len(key)]
        decoded_c = chr((ord(character) - ord(key_c) + 256) % 256)
        decoded_chars.append(decoded_c)
    plaintext = "".join(decoded_chars)
    return plaintext

def read_env_contents():
    """
    Returns enviroment variables contents as dictionary
    """
    if is_enviroment_file_present():
        with open(
            file=os.path.join(root_path, ".env"),
            mode="r",
            encoding="utf-8",
        ) as env_file_name:
            ciphertext = env_file_name.read()
            plaintext = decode(ciphertext) 
            try:
                variables = json.loads(plaintext)
            except:
                logging.debug("Failed to parse enviroment file!")
                return None, None
            else:
                return variables["email"], variables["password"]

def write_enviroment_variables(email, password):
    """
    Write enviroment variables to .env file
    """
    variables = {
        "email": email,
        "password": password    
    }
    json_env = json.dumps(variables)
    with open(
        os.path.join(root_path, ".env"), "w", encoding="utf-8"
    ) as env_file_name:
        
        ciphertext = encode(json_env)       # Encode to ciphertext
        env_file_name.write(ciphertext)     # Write ciphertext to .env