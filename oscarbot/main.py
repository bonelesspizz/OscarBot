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
@commands.is_owner()
async def load(ctx, extension):
    oscar.load_extension(f'cogs.{extension}')
    await ctx.send(f"Cog *{extension}* loaded")

@oscar.command()
@commands.is_owner()
async def unload(ctx, extension):
    oscar.unload_extension(f'cogs.{extension}')
    await ctx.send(f"Cog *{extension}* unloaded")

@oscar.command()
@commands.is_owner()
async def reload(ctx, extension):
    oscar.reload_extension(f'cogs.{extension}')
    await ctx.send(f"Cog *{extension}* reloaded")


for filename in os.listdir("."):
    if filename.endswith(".py"):
        oscar.load_extension(f"cogs.{filename[:-3]}")

oscar.run(token)
