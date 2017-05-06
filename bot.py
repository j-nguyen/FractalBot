from discord.ext import commands
import discord
import asyncio
import logging
import json

# Logger Configuration
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
log.addHandler(handler)

# Load the bot

initExt = []

desc = """
Discord bot that checks out your game stats, rankings, and much more.
"""

bot = commands.Bot(command_prefix=['?'], description=desc, pm_help=None, help_attrs=dict(hidden=True))


# Loads the configuration files
def loadFiles():
	with open('config.json') as f:
		return json.load(f)

if __name__ == '__main__':
	# load in the credentials
	config = loadFiles()

	# attempt to get the bot stuff
	bot.client_id = config['client_id']

	# Run the bot
	bot.run(config['token'])

	# unload all the handlers
	handlers = log.handlers[:]
	for hldr in handlers:
		hdlr.close()
		log.removeHandler(hdlr)

