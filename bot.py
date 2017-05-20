from discord.ext import commands
from sqlalchemy import create_engine
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
    'cogs.mod',
    # 'cogs.game'
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

@bot.event
async def on_ready():
    print('Logged in as:')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()

@bot.event
async def on_message_edit(before, after):
    # get the user 
    usr = before.author

    # send message as embed
    e = discord.Embed(colour=discord.Colour.dark_gold())
    e.set_thumbnail(url=usr.avatar_url or usr.default_avatar_url)
    e.timestamp = usr.created_at
    e.set_footer(text='Edited')
    e.set_author(name=str(usr))
    e.add_field(name='Before', value=before.content)
    e.add_field(name='After', value=after.content)
    channel = bot.get_channel(config['mod_log'])

    # send message
    try:
        await bot.send_message(channel, embed=e)
    except Exception as e:
        print ('Error: ' + str(e))

@bot.event
async def on_message_delete(message):
    usr = message.author

    # send message as embed
    e = discord.Embed(colour=discord.Colour.dark_gold())
    e.set_thumbnail(url=usr.avatar_url or usr.default_avatar_url)
    e.timestamp = datetime.datetime.utcnow()
    e.set_footer(text='Deleted')
    e.set_author(name=str(usr))
    e.add_field(name='Deleted Message', value=message.content)
    channel = bot.get_channel(config['mod_log'])

    # send message
    await bot.send_message(channel, embed=e)

@bot.event
async def on_member_join(member):
    # Create an embed and attempt to join
    e = discord.Embed(title='Member Joined', colour=discord.Colour.green())
    e.set_thumbnail(url=member.avatar_url or member.default_avatar_url)
    e.timestamp = member.joined_at
    e.set_author(name=str(member))
    e.set_footer(text='Member Joined')

    channel = bot.get_channel(config['mod_log'])

    await bot.send_message(channel, embed=e)

@bot.event
async def on_member_remove(member):
    # Create an embed and attempt to join
    e = discord.Embed(title='Member Left', colour=discord.Colour.green())
    e.set_thumbnail(url=member.avatar_url or member.default_avatar_url)
    e.timestamp = datetime.datetime.utcnow()
    e.set_author(name=str(member))
    e.set_footer(text='Member Left')

    channel = bot.get_channel(config['mod_log'])

    await bot.send_message(channel, embed=e)

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
        hldr.close()
        log.removeHandler(hldr)

