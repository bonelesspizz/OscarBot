import discord
from discord.ext import commands
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

oscar = commands.Bot(command_prefix='!')

@oscar.command()
async def load(ctx, extension):
    oscar.load_extension(f'cogs.{extension}')

oscar.run(token)
