from discord.ext import commands
import discord
import logging
import perms

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
    async def kick(self, *, member : discord.Member):
        if 
        try:
            await self.bot.kick(member)
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to kick this member.')
        except discord.HTTPException:
            await self.bot.say('Attempt to kick failed.')
        else:
            await self.bot.say('Unknown error')

    
# Helps us add to the extension
def setup(bot):
    bot.add_cog(Mod(bot))
