import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, oscar):
        self.oscar = oscar

    @commands.command()
    async def ban(self, ctx, member:discord.Member=None, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned.")

    @commands.command()
    async def unban(self, ctx, user:discord.User=None):
        await user.unban(reason=reason)
        await ctx.send(f"{member.mention} has been unbanned.")

def setup(oscar):
    oscar.add_cog(Moderation(oscar))
