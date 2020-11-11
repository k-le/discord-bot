# bot.py
# test bot to explore Discord API and its functionality

import os
import discord
import discord.ext
import random
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

# //-------------------------------------------------------
@client.event
# on_member_join() handles the event of a new member joining a guild/server
async def on_member_join(member):
    # the await keyword prevents the coroutine from executing until other coroutine has been executed
    # creates a DM channel with the user
    await member.create_dm()
    # after awaiting the creation of a DM channel, sends a message to the already existing DM channel
    await member.dm_channel.send(
        f'Hello {member.name}, welcome to my Discord server!'
    )

# //-------------------------------------------------------
@client.event
async def on_message(message):
    # this if statement checks if the one who sent the message is an actual user,
    # preventing it from a potentially recursive case where the bots (or clients) keep repeating
    if message.author == client.user:
        # 'return' is used similarly to break, the purpose is to exit the function
        return

    jojo_quotes = [
        'ORA ORA ORA ORA!!!',
        'MUDA MUDA MUDA MUDA MUDA MUDA MUDA MUDA MUDA MUDA!!'
    ]

    if message.content == 'JOJO':
        response = random.choice(jojo_quotes)
        await message.channel.send(response)
    # this elif statement allows the on_message handler to raise a DiscordException on command via 'raise-exception'
    elif message.content == 'raise-exception':
        raise discord.DiscordException

# this function will catch the DiscordException and write it to a file rather than just printing out the
# error message in the console
async def on_error(event, *args, **kwargs):
    # with statement in Python ensures proper acquisition and release of resources, in this case, files
    # i.e., it's cleaner and doesn't require a file.close() statement since it does it already
    with open('err.log', 'a') as file:
        if event == 'on_message':
            file.write(f'Unhandled message: {args[0]}\n')
        else:
            # the simple raise statement allows the exception to be re-raised and is printed in the console instead
            raise


# run the bot with its own login token
client.run(TOKEN)

