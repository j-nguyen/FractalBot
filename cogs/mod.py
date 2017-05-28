from discord.ext import commands
from .utils import db
from .utils import models
from .utils import perms
from sqlalchemy.orm import sessionmaker
import discord
import datetime

class Mod:
    """ Moderation related commands """

    def __init__(self, bot):
        self.bot = bot
        # Set-up the engine here.
        self.engine = db.engine
        # Create a session
        self.Session = sessionmaker(bind=self.engine)

    @commands.command()
    @perms.mod_or_permissions(kick_members=True)
    async def whois(self, user: discord.Member):
        e = discord.Embed(title='Member Information', colour=discord.Colour.red())
        e.set_thumbnail(url=user.avatar_url or user.default_avatar_url)
        e.timestamp = datetime.datetime.utcnow()
        e.set_author(name=str(user))
        e.add_field(name='Member Joined:', value=user.joined_at)
        e.add_field(name='Roles', value=', '.join([str(role) for role in user.roles if str(role) != '@everyone']))
        e.add_field(name='Nickname:', value=user.nick)
        e.set_footer(text='ID: {}'.format(user.id))

        await self.bot.say(embed=e)


    @commands.command(pass_context=True)
    @perms.mod_or_permissions(kick_members=True)
    async def prune(self, ctx, msg: int):
        if msg <= 0:
            await self.bot.say('Cannot delete less than 0 messages, dumbass.')
        else:
            channel = ctx.message.channel

            deleted = await self.bot.purge_from(channel, limit=msg)
            await self.bot.say('Deleted {} messages.'.format(len(deleted)))

    @commands.command(pass_context=True)
    # @perms.mod_or_permissions(administrator=True)
    async def addmembers(self, ctx):
        """ This command will ERASE, and CREATE all members currently in the server. Be careful using this """

        server = ctx.message.server



# Helps us add to the extension
def setup(bot):
    bot.add_cog(Mod(bot))
