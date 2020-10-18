import discord
from dotenv import load_dotenv
import os

load_dotenv('.env')
token = os.getenv('DISCORD_TOKEN')

oscar = discord.Client()

@oscar.event
async def on_ready():
    print("Ready")

oscar.run(token)
