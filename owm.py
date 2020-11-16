"""
Functions used to grab weather data via OpenWeatherMap API, intended for !weather {postal_code} command for Discord bot
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()
OWMKey = os.getenv('OWM_API')   # load OpenWeatherMap API key for parsing JSON data

def get_weather_dict(postal_code):
    """
    sends an API call to OpenWeatherMap for weather JSON object
    :param postal_code: String, 5-digit postal code representing location in the US
    :return: Dictionary, nested dictionary containing weather data
    """
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?zip={postal_code},US&appid={OWMKey}')
    return response.json()

def get_postal_code():
    """
    prompts the User to enter a 5-digit postal code
    :return: String, postal code
    """
    postal_code = str(input("Please enter a postal code: "))
    return postal_code

def get_weather_id(weather_dict):
    """
    grabs weather ID from weather data to identify weather conditions
    :param weather_dict: Dictionary, contains weather info from OWM
    :return: Int, weather id for identifying weather conditions
    """
    return weather_dict['weather'][0]['id']

def get_weather_conditions(weather_id):
    """
    takes in a weather ID from OWM and returns a weather condition
    :param weather_id: Int, weather id for identifying weather conditions
    :return: String, weather condition
    """
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
    """
    grabs temperature from weather data and converts it to degrees Fahrenheit
    :param weather_dict: Dictionary, contains weather info from OWM
    :return: String, temperature in degrees Fahrenheit, formatted to 1 decimal place
    """
    kelvin = weather_dict['main']['temp']
    fahrenheit = ((kelvin - 273.15) * (9/5) + 32)
    return '{0:.3g}'.format(fahrenheit)

def get_wind(weather_dict):
    """
    grabs wind speeds from weather data and converts it to mph
    :param weather_dict: Dictionary, contains weather info from OWM
    :return: String, wind speeds in mph, formatted to 1 decimal place
    """
    wind_speed = weather_dict['wind']['speed']
    return '{0:.3g}'.format(wind_speed*2.237)

def get_humidity(weather_dict):
    """
    grabs humidity levels from weather data
    :param weather_dict: Dictionary, contains weather info from OWM
    :return: Int, humidity level from 0-100
    """
    return weather_dict['main']['humidity']
