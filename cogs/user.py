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
    async def join(self, role: str):
        pass

# Helps us add to the extension
def setup(bot):
    bot.add_cog(User(bot))
