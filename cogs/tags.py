from discord.ext import commands
from .utils import db
from .utils import models
from .utils import perms
from sqlalchemy.orm import sessionmaker
import discord
import logging


# Enables us to get a specific log for each extension
log = logging.getLogger(__name__)

class Tags:
    def __init__(self, bot):
        self.bot = bot
        # Set-up the engine here.
        self.engine = db.engine
        # Create a session
        self.Session = sessionmaker(bind=self.engine)

    # We will need a command to insert a new tag into the db.
    @commands.group(pass_context=True)
    @perms.mod_or_permissions(kick_members=True)
    async def tag(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid tag command passed')

    @tag.command()
    @perms.mod_or_permissions(kick_members=True)
    async def add(self, name: str, *, desc: str):
        # Create a tag object
        tag = models.Tag(name=name, description=desc)

        sess = self.Session()

        try:
            sess.add(tag)
            sess.commit()
            await self.bot.say('Added tag command.')
        except Exception as e:
            await self.bot.say(e)
        finally:
            sess.close()


# Helps us add to the extension
def setup(bot):
    bot.add_cog(Tags(bot))