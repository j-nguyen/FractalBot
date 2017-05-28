from discord.ext import commands
from .utils import db
from .utils import models
from .utils import perms
from sqlalchemy.orm import sessionmaker
import discord
import datetime

class User:
    """ User related commands """

    def __init__(self, bot):
        self.bot = bot
        # Set-up the engine here.
        self.engine = db.engine
        # Create a session
        self.Session = sessionmaker(bind=self.engine)

    # Lets the user join a specific role which opens up a channel for them.
    @commands.command(pass_context=True)
    async def join(self, ctx, role: discord.Role = None):
        member = ctx.message.author

        if role != None:
            try:
                await self.bot.add_roles(member, role)
                await self.bot.say("Joined {}.".format(str(role)))
            except discord.Forbidden:
                await self.bot.say('Cannot add')
            except discord.HTTPException:
                await self.bot.say('Adding roles failed!')
        else:
            await self.bot.say('That is not a role.')


# Helps us add to the extension
def setup(bot):
    bot.add_cog(User(bot))
