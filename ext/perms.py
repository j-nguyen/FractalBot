# permissions to check for commands
# We'll attempt to load from the file again as well.
from discord.ext import commands
import discord.utils

# Checks mod permissions
# This is the only one we really need.
# TODO: Fix this, as it's a bare type of a function
def check_permissions(ctx):
    # Get the user
    usr = ctx.message.author

    # Attempt to find the permissions from the author
    roles = usr.roles

    # Check to see if a specified role is in
    return any(role.name == 'Staff' for role in roles)
