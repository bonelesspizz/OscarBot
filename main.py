import discord
from discord.ext import commands
import dotenv
from dotenv import load_dotenv
import os
import sqlite3
from sqlite3 import Error

load_dotenv() # Loads the key,value from .env
token = os.getenv('DISCORD_TOKEN') # Sets the token variable to the value in .env

intents = discord.Intents.default()
intents.members = True # Enables the members intent to be used, which allows for on_member_join() and other member related functions
intents.guilds = True

oscar = commands.Bot(command_prefix='!', intents=intents) # Sets the intents

@oscar.event
async def on_ready():
    print("Ready")
    await oscar.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("!help"))

for filename in os.listdir('./oscarbot'):
    if filename.endswith(".py") and filename != "utils.py":
        oscar.load_extension(f"oscarbot.{filename[:-3]}")

def create_connection(db_file):
    try:
        # Create database if it does not exist
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS warns(member TEXT, reasons TEXT, total INTEGER)""")
    except Error as e:
        print(e)
    finally:
        # if successful connection
        if conn:
            conn.close()

create_connection("warnslist.db")

oscar.run(token)
