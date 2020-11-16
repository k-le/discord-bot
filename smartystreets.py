"""
Functions used to grab location data via SmartyStreets API, intended for !weather {postal_code} command for Discord bot
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()
AUTH_ID = os.getenv('SmartyStreets_ID')         # load authentication ID for SmartyStreets
AUTH_TOKEN = os.getenv('SmartyStreets_TOKEN')   # load authentication Token for SmartyStreets


def get_loc_dict(postal_code):
    """
    takes in a 5-digit postal code in the US and returns a dictionary containing location data parsed from SmartyStreets JSON object
    :param postal_code: Int, 5-digit postal code in the US
    :return: Dictionary, nested dictionary containing location data
    """
    response = requests.get(f'https://us-zipcode.api.smartystreets.com/lookup?auth-id={AUTH_ID}&auth-token={AUTH_TOKEN}&zipcode={postal_code}')
    return response.json()

def get_state(loc_dict):
    """
    grabs abbreviated state from location data
    :param loc_dict: Dictionary, contains location data
    :return: String, abbreviated state, e.g. MN, IA, CA, NY
    """
    return loc_dict[0]['city_states'][0]['state_abbreviation']

def get_city(loc_dict):
    """
    grabs the top city (most populated) in the dictionary from location data
    :param loc_dict: Dictionary, contains location data
    :return: String, most populated city at/near the given location
    """
    return loc_dict[0]['city_states'][0]['city']