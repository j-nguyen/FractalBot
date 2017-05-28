from discord.ext import commands
from .utils import db
from .utils import models
from .utils import perms
from sqlalchemy.orm import sessionmaker

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
            await self.bot.say('Invalid tag command. $tag <add/remove/list/show>')

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
            await self.bot.say('Cannot add. Reasons: Duplicate entry, or Invalid response.')
        finally:
            sess.close()

    @tag.command()
    @perms.mod_or_permissions(kick_members=True)
    async def remove(self, name: str):
        # Removes the tag

        sess = self.Session()

        tag = sess.query(models.Tag).filter(models.Tag.name == name).first()

        if tag != None:
            sess.delete(tag)
            sess.commit()
            await self.bot.say('Tag *{}* deleted.'.format(name))
        else:
            await self.bot.say('Cant find the specified tag!')

    @tag.command()
    async def list(self):
        # Shows the list of tags
        sess = self.Session()

        tags = sess.query(models.Tag).all()

        if tags is None:
            await self.bot.say('No tags.')
        else:
            tagsName = [tag.name for tag in tags]
            await self.bot.say('Tags: ' + ', '.join(tagsName))

    @tag.command()
    async def show(self, name: str):
        # display the tag
        sess = self.Session()

        tag = sess.query(models.Tag).filter(models.Tag.name == name).first()

        if tag is None:
            await self.bot.say('Tag cannot be found.')
        else:
            await self.bot.say('{}'.format(tag.description))

# Helps us add to the extension
def setup(bot):
    bot.add_cog(Tags(bot))