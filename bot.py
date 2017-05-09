from discord.ext import commands
import discord
import asyncio
import logging
import json
import datetime

# Logger Configuration
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
log.addHandler(handler)

# Load the bot

initExt = [
    'cogs.mod'
]

desc = """
Discord bot that checks out your game stats, rankings, and much more.
"""

bot = commands.Bot(command_prefix=['$'], description=desc, pm_help=None, help_attrs=dict(hidden=True))

# Bot events

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')

@bot.event
async def on_ready():
    print('Logged in as:')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()

@bot.event
async def on_message(message):
    await bot.process_commands(message)

# Loads the configuration files
def loadFiles():
    with open('config.json') as f:
        return json.load(f)

if __name__ == '__main__':
    # load in the credentials
    config = loadFiles()

    # attempt to get the bot stuff
    bot.client_id = config['client_id']

    # Attempt to load the extensions
    for ext in initExt:
            try:
                bot.load_extension(ext)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(ext, type(e).__name__, e))

    # Run the bot
    bot.run(config['token'])

    # unload all the handlers
    handlers = log.handlers[:]
    for hldr in handlers:
                hdlr.close()
                log.removeHandler(hdlr)

