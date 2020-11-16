# bot_subclass.py
# testing bot subclass from Discord extensions package

import owm
import smartystreets
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
# Discord Token
TOKEN = os.getenv('DISCORD_TOKEN')

# OpenWeatherMap API Key
OWMKey = os.getenv('OWM_API')

# instead of the Client superclass, we utilize the Bot subclass
bot = commands.Bot(command_prefix='!')

# on_ready() called when bot has finished setting up
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# //-------------------------------------------------------
# bots must utilize arbitrary keywords (set by the programmer) for events to be called
# bot.command() takes in an argument, which allows the function to be called whenever the argument is mentioned

# //-------------------------------------------------------
# weather command
@bot.command(name='weather', help='Given a 5-digit postal-code, will print out details about the current weather for that location')
async def weather(ctx, postal_code):
    """
    takes in a 5-digit postal code and prints out details about the current weather for the location
    utilizes OpenWeatherMap API for weather information and SmartyStreets API for location
    :param ctx: Context for bot
    :param postal_code: Int, 5-digit postal code for location purposes
    :return:
    """
    weather_dict = owm.get_weather_dict(postal_code)    # creates a nested dictionary of weather info from parsed OpenWeatherMap JSON object
    loc_dict = smartystreets.get_loc_dict(postal_code)  # creates a nested dictionary of location info from parsed SmartyStreets JSON object

    weather_id = owm.get_weather_id(weather_dict)   # grabs weather id to identify weather conditions
    weather_cond = owm.get_weather_conditions(weather_id)   # weather conditions based on id parsed, snow, rain, clouds, etc.

    temp = owm.get_temperature(weather_dict)    # grabs temperature in fahrenheit
    wind_speed = owm.get_wind(weather_dict)     # wind speeds in mph
    humidity = owm.get_humidity(weather_dict)   # humidity percentage

    city = smartystreets.get_city(loc_dict)     # grabs city
    state = smartystreets.get_state(loc_dict)   # state

    await ctx.send(f'{city}, {state} \n'        # prints out a formatted response detailing the current weather of the
                   f'{temp}° F \n'              # given location into the server channel where the command was called
                   f'Currently {weather_cond} \n'
                   f'Winds at {wind_speed}mph \n'
                   f'{humidity}% Humidity')

bot.run(TOKEN)

