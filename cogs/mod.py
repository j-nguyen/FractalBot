from discord.ext import commands
from .utils import perms
import discord
import logging

# Enables us to get a specific log for each extension
log = logging.getLogger(__name__)

class Mod:
    """ Moderation related commands """

    def __init__(self, bot):
        self.bot = bot

    # Command to kick the user.
    # Paramaters:
    # - discord.Member class Object.
    # Returns:
    # - Sends a discord message, returns or not.
    @commands.command(no_pm=True)
    @perms.mod_or_permissions(kick_members=True)
    async def kick(self, *, member : discord.Member):
        try:
            await self.bot.kick(member)
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to kick this member.')
        except discord.HTTPException:
            await self.bot.say('Attempt to kick failed.')
        else:
            await self.bot.say('{0.name} kicked'.format(member))

    
# Helps us add to the extension
def setup(bot):
    bot.add_cog(Mod(bot))
