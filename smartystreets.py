import requests
import os
from dotenv import load_dotenv

load_dotenv()
AUTH_ID = os.getenv('SmartyStreets_ID')
AUTH_TOKEN = os.getenv('SmartyStreets_TOKEN')

# https://us-zipcode.api.smartystreets.com/lookup?auth-id={AUTH_ID}&auth-token={AUTH_TOKEN}&zipcode={postal_code}

def get_loc_dict(postal_code):
    response = requests.get(f'https://us-zipcode.api.smartystreets.com/lookup?auth-id={AUTH_ID}&auth-token={AUTH_TOKEN}&zipcode={postal_code}')
    return response.json()

def get_state(loc_dict):
    return loc_dict[0]['city_states'][0]['state_abbreviation']
