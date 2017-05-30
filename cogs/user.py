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

    @commands.group(pass_context=True)
    async def topic(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid command: $tag <list/join/leave>')

    # Lets the user join a specific role which opens up a channel for them.
    @topic.command(pass_context=True)
    async def join(self, ctx, name: str = None):
        """ Joins a specific topic, given the topic name """
        member = ctx.message.author
        roles = ctx.message.server.roles

        if name is None:
            await self.bot.say('Are you sure you\'ve inputted something?')
        else:
            db = self.Session()
            topic = db.query(models.Topic).filter(models.Topic.name == name).first()
            db.close()
            if topic:
                role = discord.utils.find(lambda r: r.id == str(topic.role_id), roles)
                try:
                    await self.bot.add_roles(member, role)
                    await self.bot.say('Joined {}'.format(topic.name))
                except discord.Forbidden:
                    await self.bot.say('Cannot add! Permissions wrong?')
                except discord.HTTPException:
                    await self.bot.say('Something happened! Please try again')
            else:
                await self.bot.say('Could not find topic channel.')

    @topic.command()
    async def list(self):
        """ List all the topics available. """
        db = self.Session()
        topics = db.query(models.Topic).all()
        db.close()

        await self.bot.say('Topics: {}'.format(','.join([topic.name for topic in topics])))

    @topic.command()
    @perms.mod_or_permissions(kick_members=True)
    async def add(self, name: str, role: discord.Role = None):
        """ Adds a topic """
        if role is None:
            await self.bot.say('Invalid role.')
        else:
            try:
                db = self.Session()
                topic = models.Topic(name=name, role_id=role.id)
                db.add(topic)
                db.commit()
                await self.bot.say('Added topic.')
            except Exception as e:
                print (e)

    @topic.command(pass_context=True)
    async def leave(self, ctx, name: str = None):
        """ Leave a topic that you are from. """
        if name is None:
            await self.bot.say('Invalid topic.')
        else:
            member = ctx.message.author
            roles = ctx.message.author.roles

            db = self.Session()
            topic = db.query(models.Topic).filter(models.Topic.name == name).first()
            db.close()

            if topic:
                try:
                    role = discord.utils.find(lambda r: r.id == str(topic.role_id), roles)
                    await self.bot.remove_roles(member, role)
                    await self.bot.say('Left {} topic.'.format(topic.name))
                except discord.Forbidden:
                    await self.bot.say('Something went wrong')
                except discord.HTTPException:
                    await self.bot.say('Leaving role failed')

    @topic.command()
    @perms.mod_or_permissions(kick_members=True)
    async def remove(self, name: str = None):
        """ Removes a topic from the database. """
        if name is None:
            await self.bot.say('Invalid topic')
        else:
            db = self.Session()

            try:
                topic = db.query(models.Topic).filter(models.Topic.name == name).first()
                db.delete(topic)
                db.commit()

                await self.bot.say('Deleted {} topic'.format(topic.name))
            except Exception as e:
                print (e)
            finally:
                db.close()

# Helps us add to the extension
def setup(bot):
    bot.add_cog(User(bot))
