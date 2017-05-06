from discord.ext import commands
import discord
import asyncio
import logging

# Loads the configuration files
def loadFiles():
	with open('config.json') as f:
		return json.load(f)
		

if __name__ == '__main__':
	main()