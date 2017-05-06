from discord.ext import commands
import discord
import logging

# Enables us to get a specific log for each extension
log = logging.getLogger(__name__)

class Mod:
    """ Moderation related commands """

    def __init__(self, bot):
        self.bot = bot

# Helps us add to the extension
def setup(bot):
    bot.add_cog(Mod(bot))
