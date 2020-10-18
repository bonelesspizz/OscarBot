import discord
from discord.ext import commands
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

oscar = commands.Bot(command_prefix='!')

@oscar.event
async def on_ready():
    print("Ready")

@oscar.command()
async def load(ctx, extension):
    oscar.load_extension(f'cogs.{extension}')

@oscar.command()
async def unload(ctx, extension):
    oscar.unload_extension(f'cogs.{extension}')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        oscar.load_extension(f"cogs.{filename[:-3]}")


oscar.run(token)
