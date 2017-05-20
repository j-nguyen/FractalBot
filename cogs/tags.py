from discord.ext import commands
from .utils import perms
import discord
import logging

# Enables us to get a specific log for each extension
log = logging.getLogger(__name__)

class Tags:
    def __init__(self, bot):
        self.bot = bot

    # We will need a command to insert a new tag into the db.
    @commands.group(pass_context=True)
    @perms.mod_or_permissions(kick_members=True)
    async def tag(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid tag command passed')

    @tag.command()
    @perms.mod_or_permissions(kick_members=True)
    async def add(self, name: str, *, desc: str):


# Helps us add to the extension
def setup(bot):
    bot.add_cog(Tags(bot))