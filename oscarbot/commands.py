import discord
from discord.ext import commands
import random
from datetime import datetime
import time
from .utils import words


class Commands(commands.Cog):
    def __init__(self, oscar):
        self.oscar = oscar

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.oscar.load_extension(f'cogs.{extension}')

        embed = discord.Embed(title="Cogs", description=f"Cog {extension} loaded", timestamp=datetime.now(), color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Load cog", icon_url="attachment://logo.png")
        await ctx.send(file=logo,embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.oscar.unload_extension(f'cogs.{extension}')

        embed = discord.Embed(title="Cogs", description=f"Cog {extension} unloaded", timestamp=datetime.now(), color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Unload cog", icon_url="attachment://logo.png")
        await ctx.send(file=logo,embed=embed)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.oscar.reload_extension(f'cogs.{extension}')

        embed = discord.Embed(title="Cogs", description=f"Cog {extension} reloaded", timestamp=datetime.now(), color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Reload cog", icon_url="attachment://logo.png")
        await ctx.send(file=logo,embed=embed)

    @commands.command(name="8ball")
    async def _8ball(self, ctx, question):
        answers = ["As I see it, yes.",
                   "Ask again later.",
                   "Better not tell you now.",
                   "Cannot predict now.",
                   "Concentrate and ask again.",
                   "Don’t count on it.",
                   "It is certain.",
                   "It is decidedly so.",
                   "Most likely.",
                   "My reply is no.",
                   "My sources say no.",
                   "Outlook not so good.",
                   "Outlook good.",
                   "Reply hazy, try again.",
                   "Signs point to yes.",
                   "Very doubtful.",
                   "Without a doubt.",
                   "Yes.",
                   "Yes – definitely.",
                   "You may rely on it."]

        result = random.choice(answers)

        embed = discord.Embed(title="8Ball is rolling...", description=result, timestamp=datetime.now(), color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="8ball", icon_url="attachment://logo.png")
        await ctx.send(file=logo,embed=embed)

    @commands.command()
    async def typingtest(self, ctx, *length):
        if length:
            length = int("".join(length[0]))
        else:
            length = 10
        
        user_id = ctx.message.author.id

        text = " ".join([random.choice(words) for w in range(length)])
        await ctx.send(f"`{text}`") 

        now = datetime.now()
        elapsed_time = 0
        while True:
            time.sleep(1)
            elapsed_time += 1
            async for message in ctx.message.channel.history(after=now):
                if message.author.id == user_id:
                        cont = (message.content).split(" ")
                        wpm = int(round(len(cont)) / (elapsed_time/60))
                        acc = (len(cont) / length) * 100
                        await ctx.send(f"{ctx.message.author.mention} {wpm}WPM, {int(acc)}% accuracy")
                        return

def setup(oscar):
    oscar.add_cog(Commands(oscar))
