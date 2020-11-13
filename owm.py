import smartystreets
import requests
import os
from dotenv import load_dotenv

load_dotenv()
OWMKey = os.getenv('OWM_API')

def get_weather_dict(postal_code):
    """
    sends an API call to OpenWeatherMap for weather JSON data
    :param postal_code: String, 5-digit postal code representing location in the US
    :return: None
    """
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?zip={postal_code},US&appid={OWMKey}')
    return response.json()

def get_postal_code():
    """
    prompts the User to enter a 5-digit postal code
    :return: String
    """
    postal_code = str(input("Please enter a postal code: "))
    return postal_code

def get_weather_id(weather_dict):
    return weather_dict['weather'][0]['id']

def get_weather_conditions(weather_id):
    weather_conditions = {range(200, 233): 'Thunderstorm',
                          range(300, 322): 'Drizzle',
                          range(500, 532): 'Rain',
                          range(600, 623): 'Snow',
                          800: 'Clear',
                          801: 'Mostly CLear',
                          802: 'Partly Cloudy',
                          803: 'Mostly Cloudy',
                          804: 'Overcast Clouds'
                          }

    return weather_conditions[weather_id]

def get_temperature(weather_dict):
    kelvin = weather_dict['main']['temp']
    fahrenheit = ((kelvin - 273.15) * (9/5) + 32)
    return fahrenheit

def get_city(weather_dict):
    return weather_dict['name']



postal_code = get_postal_code()
weather_dict = get_weather_dict(postal_code)
weather_id = get_weather_id(weather_dict)
print(get_weather_conditions(weather_id))


loc_dict = smartystreets.get_loc_dict(smartystreets.AUTH_ID, smartystreets.AUTH_TOKEN, postal_code)
print(smartystreets.get_state(loc_dict))
