from discord.ext import commands
from .utils import db
from .utils import models
from .utils import perms
from sqlalchemy.orm import sessionmaker
import discord
import datetime
import asyncio

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
        """ Find information about the current member """
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
        """ Purges messages based on the number of messages given. """
        if msg <= 0:
            await self.bot.say('Cannot delete less than 0 messages, dumbass.')
        else:
            channel = ctx.message.channel

            deleted = await self.bot.purge_from(channel, limit=msg)
            botMsg = await self.bot.say('Deleted {} messages.'.format(len(deleted)))
            # Wait 5 seconds
            await asyncio.sleep(3)
            await self.bot.delete_message(botMsg);


    @commands.command(pass_context=True)
    @perms.mod_or_permissions(administrator=True)
    async def addmembers(self, ctx):
        """ Adds all unique members into the DB, if not configured. """
        server = ctx.message.server
        usrs = server.members

        usersDB = []

        # Attempt to add to the user.
        for usr in usrs:
            if not usr.bot:
                usersDB.append(models.User(name=str(usr)))

        # Insert
        try:
            db = self.Session()
            for user in usersDB:
                q = db.query(models.User).filter(models.User.name == user.name)
                if not db.query(q.exists()).scalar():
                    db.add(user)
            db.commit()

            await self.bot.say('Added all members.')
        except Exception as e:
            print (e)
        finally:
            db.close()

    @commands.group(pass_context=True)
    @perms.mod_or_permissions(administrator=True)
    async def rankLevel(self, ctx):
        """ Adds a rank like an achievement to a rank """
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid command: $rankLevel <add/remove/list>')

    @rankLevel.command()
    async def list(self):
        db = self.Session()

        try:
            ranks = db.query(models.Role).all()
            # TODO: Show the rank names (roles)
            rankList = [rank.id for rank in ranks]

            await self.bot.say('Ranks: {}'.format(', '.join(rankList)))
        except Exception as e:
            print (e)
        finally:
            db.close()


    @rankLevel.command()
    async def add(self, role : discord.Role = None, level : int = 0):
        if role is None:
            await self.bot.say('You did not insert a role.')
        else:
            db = self.Session()

            try:
                rank = models.Role(role_id=role.id, rank_id=level)

                db.add(rank)
                db.commit()

                await self.bot.say('Added new level role achievement.')
            except Exception as e:
                print (e)
            finally:
                db.close()

    @rankLevel.command()
    async def remove(self, role: discord.Role = None):
        if role is None:
            await self.bot.say('You did not enter a role id.')
            return

        db = self.Session()

        try:
            rank = db.query(models.Role).filter(models.Role.role_id == role.id).first()

            if rank is not None:
                db.delete(rank)
                db.commit()

                await self.bot.say('Deleted rank role')
        except Exception as e:
            print (e)



# Helps us add to the extension
def setup(bot):
    bot.add_cog(Mod(bot))
