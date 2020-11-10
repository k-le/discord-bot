# bot.py
# test bot to explore Discord API and its functionality

import os
import discord
from dotenv import load_dotenv


# environment variables are those that exist outside of the project's code as part of the server environment
# load_dotenv() loads environment variables from a file named .env in the current directory
load_dotenv()

# calls environment-related method as provided by os.getenv()
# here, we read it into the code from an environment variable:
TOKEN = os.getenv('DISCORD_TOKEN')
"""
important to use environment variables when working with secrets (such as Discord tokens) and also when
using different variables for development/production environments w/o changing code
this means that this code can work in varying environments compared to just a single environment
"""

# creates an instance of a client connection to Discord to interact with Discord API
client = discord.Client()

# registers an event to listen to
@client.event
# asynchronous means the event is done in a "callback" style, meaning the function is called when something happens, not on its own
# on_ready() is an event called when the bot has finished logging in
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# run the bot with its own login token
client.run(TOKEN)

