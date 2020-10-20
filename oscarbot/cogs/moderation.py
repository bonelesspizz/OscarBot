import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, oscar):
        self.oscar = oscar

    @commands.command()
    async def ban(self, ctx, user, reason):
        await guild.ban(user,*,reason=reason, delete_message_days=0)
        await ctx.send(f"{user.mention} has been banned.")

def setup(oscar):
    oscar.add_cog(Moderation(oscar))
