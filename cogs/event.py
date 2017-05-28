from discord.ext import commands
from sqlalchemy.orm import sessionmaker
from .utils import models
from .utils import db
import discord
import datetime
import json

class Event:
    """ Discord Events """

    def __init__(self, bot):
        self.bot = bot
        self.config = self.loadConfig()
        # Set-up the engine here.
        self.engine = db.engine
        # Create a session
        self.Session = sessionmaker(bind=self.engine)

    def loadConfig(self):
        with open('config.json') as f:
            return json.load(f)

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.NoPrivateMessage):
            await self.bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')

    async def on_ready(self):
        print('Logged in as:')
        print('Username: ' + self.bot.user.name)
        print('ID: ' + self.bot.user.id)
        print('------')

    async def on_message_edit(self, before, after):
        # Make sure the contents are the same
        if before.content == after.content:
            return

        # get the user
        usr = before.author

        # send message as embed
        e = discord.Embed(colour=discord.Colour.dark_gold())
        e.set_thumbnail(url=usr.avatar_url or usr.default_avatar_url)
        e.timestamp = usr.created_at
        e.set_footer(text='ID: {}'.format(usr.id))
        e.set_author(name=str(usr))
        e.add_field(name='Before', value=before.content)
        e.add_field(name='After', value=after.content)
        channel = self.bot.get_channel(self.config['mod_log'])

        # send message
        try:
            await self.bot.send_message(channel, embed=e)
        except Exception as e:
            print('Error: ' + str(e))

    async def on_message_delete(self, message):
        usr = message.author

        # send message as embed
        e = discord.Embed(colour=discord.Colour.dark_gold())
        e.set_thumbnail(url=usr.avatar_url or usr.default_avatar_url)
        e.timestamp = datetime.datetime.utcnow()
        e.set_footer(text='ID: {}'.format(usr.id))
        e.set_author(name=str(usr))
        e.add_field(name='Deleted Message', value=message.content)
        channel = self.bot.get_channel(self.config['mod_log'])

        # send message
        await self.bot.send_message(channel, embed=e)

    async def on_member_join(self, member):
        # Create an embed and attempt to join
        e = discord.Embed(title='Member Joined', colour=discord.Colour.green())
        e.set_thumbnail(url=member.avatar_url or member.default_avatar_url)
        e.timestamp = member.joined_at
        e.set_author(name=str(member))
        e.set_footer(text='ID: {}'.format(member.id))

        channel = self.bot.get_channel(self.config['mod_log'])

        await self.bot.send_message(channel, embed=e)

        # Attempt to insert into db for user
        db = self.Session()

        user = models.User(name=str(member))

        try:
            db.add(user)
            db.commit()
            print ("Member inserted")
        except Exception as e:
            pass
        finally:
            db.close()

    async def on_member_remove(self, member):
        # Create an embed and attempt to join
        e = discord.Embed(title='Member Left', colour=discord.Colour.red())
        e.set_thumbnail(url=member.avatar_url or member.default_avatar_url)
        e.timestamp = datetime.datetime.utcnow()
        e.set_author(name=str(member))
        e.set_footer(text='ID: {}'.format(member.id))

        channel = self.bot.get_channel(self.config['mod_log'])
        await self.bot.send_message(channel, embed=e)

        db = self.Session()

        try:
            user = db.query(models.User).filter(models.User.name == str(member)).first()
            if user is not None:
                db.remove(user)
                db.commit()
                print ("Member removed")
        except Exception as e:
            pass
        finally:
            db.close()


    async def on_message(self, message):
        await self.bot.process_commands(message)


# Helps us add to the extension
def setup(bot):
    bot.add_cog(Event(bot))
