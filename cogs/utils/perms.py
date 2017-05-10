# permissions to check for commands
# We'll attempt to load from the file again as well.
from discord.ext import commands
import discord.utils

# Checks permission based on the attribute given.
def check_permissions(ctx, perms):
    msg = ctx.message

    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())

# Checks permission based on the role.
def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None

# Checks permission for Moderators
def mod_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name == 'Staff', **perms)

    # Adds to the command import check
    return commands.check(predicate)
