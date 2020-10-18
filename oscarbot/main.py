import discord
from discord.ext import commands
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

oscar = commands.Bot(command_prefix='!')

oscar.run(token)
