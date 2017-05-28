from discord.ext import commands
import cogs.utils.db as db
import discord
import asyncio
import logging
import json
import datetime
import psycopg2

# Logger Configuration
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Bot-setup

initExt = [
    'cogs.event',
    'cogs.mod',
    'cogs.tags'
]

desc = """
Discord bot that checks out your game stats, rankings, and much more.
"""

bot = commands.Bot(command_prefix=['$'], description=desc, pm_help=None, help_attrs=dict(hidden=True))

# Loads the configuration files
def loadFiles():
    with open('config.json') as f:
        return json.load(f)

def loadDatabase():
    with open('postgresql.json') as f:
        dbFile = json.load(f)

    # Connect db
    db.loadDB(dbFile['user'], dbFile['password'], dbFile['hostname'], dbFile['database'])

if __name__ == '__main__':
    # load in the credentials
    config = loadFiles()

    # attempt to get the bot stuff
    bot.client_id = config['client_id']

    # Load db
    loadDatabase()

    # Attempt to load the extensions
    for ext in initExt:
            try:
                bot.load_extension(ext)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(ext, type(e).__name__, e))

    # Run the bot
    bot.run(config['token'])

