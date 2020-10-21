import discord
from discord.ext import commands

class OnMemberJoin(commands.Cog):
    def __init__(self, oscar):
        self.oscar = oscar

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = guild.system_channel
        await channel.send(f"Welcome {member.mention} to the server!")

def setup(oscar):
    oscar.add_cog(OnMemberJoin(oscar))
