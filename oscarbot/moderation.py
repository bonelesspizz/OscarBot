import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, oscar):
        self.oscar = oscar

    @commands.command()
    async def ban(self, member, *,reason=None):
        await member.ban(member, reason=reason)

def setup(oscar):
    oscar.add_cog(Moderation(oscar))
