import discord
from discord.ext import commands
import random
from datetime import datetime
import time
import os
import json

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

        words = open("wordlist.txt","r").readlines()

        text = " ".join([random.choice(words).strip() for n in range(length)])
        await ctx.send(f"`{text}`") 

        elapsed_time = 0.0
        start_time = datetime.utcnow()
        while True:
            time.sleep(1)
            elapsed_time += 1.0
            async for message in ctx.message.channel.history(after=start_time):
                if message.author.id == user_id:
                        cont = (message.content).split(" ")
                        wpm = int(round(len(cont)) / (elapsed_time/60))
                        acc = (len(cont) / length) * 100
                        await ctx.send(f"{ctx.message.author.mention} {wpm}WPM, {int(acc)}% accuracy")
                        return False

    @commands.command()
    async def userinfo(self, ctx, member:discord.Member=None):
        if member is None:
            member = ctx.message.author

        embed = discord.Embed(title="Info for {0}".format(member), timestamp=datetime.now(), color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Userinfo", icon_url="attachment://logo.png")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Status", value="{0}".format(member.status), inline=False)
        embed.add_field(name="Account created on", value="{0}\n({1} days ago)".format(member.created_at.strftime("%d-%m-%y at %H:%M"), (datetime.now() - member.created_at).days))
        embed.add_field(name="Joined server on", value="{0}\n({1} days ago)".format(member.joined_at.strftime("%d-%m-%y at %H:%M"), (datetime.now() - member.joined_at).days))
        embed.add_field(name="Roles", value="{0}".format(", ".join(role.mention for role in member.roles)), inline=False)
        embed.set_footer(text=f'ID: {member.id}')
        await ctx.send(file=logo, embed=embed)

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def setprefix(self, ctx, prefix):
        f = open(os.path.realpath('../Oscar Bot/prefix.json'), "r+")
        data = json.load(f)
        data["prefix"] = prefix
        f.seek(0)
        json.dump(data,f,indent=4)
        f.truncate()
        f.close()
        self.oscar.command_prefix = prefix
        await self.oscar.change_presence(status=discord.Status.do_not_disturb,activity=discord.Game(f"{prefix}help"))
        await ctx.send(f"Prefix changed to ``{prefix}``")

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Bot commands", timestamp=datetime.now(), color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Help", icon_url="attachment://logo.png")
        embed.add_field(name="Server Commands", value='load, unload, reload, setprefix', inline=False)
        embed.add_field(name="Moderation", value='ban, unban, kick, mute, unmute, warn, clearwarns', inline=False)
        embed.add_field(name="User Commands", value='8ball, userinfo, typingtest')
        await ctx.send(file=logo, embed=embed)

def setup(oscar):
    oscar.add_cog(Commands(oscar))
