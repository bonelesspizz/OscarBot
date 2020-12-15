import discord
from discord.ext import commands
from datetime import datetime

# Listeners for member joining and for when bot joins a guild
class Join(commands.Cog):
    def __init__(self, oscar):
        self.oscar = oscar

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel

        embed = discord.Embed(title="Member joined",timestamp=datetime.now(),color=discord.Colour.darker_grey())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=(f"**{member}**, welcome to **{member.guild}**"), value="** **")
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Joined a Server", icon_url="attachment://logo.png")
        embed.set_footer(text=f'ID: {member.id}')

        if channel is not None:
            await channel.send(file=logo,embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channel = guild.system_channel

        embed = discord.Embed(title="Hello, I am Oscar Bot. To get started, run !help.",timestamp=datetime.now(),color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Joined a Server", icon_url="attachment://logo.png")

        if channel is not None:
            await channel.send(file=logo,embed=embed)


def setup(oscar):
    oscar.add_cog(Join(oscar))
