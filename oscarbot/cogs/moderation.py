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
    async def unban(self, ctx, member):
        banned_users = ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban in banned_users:
            user = ban.user
            if (member_name, member_discriminator) == (user.name, user.discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned.")

def setup(oscar):
    oscar.add_cog(Moderation(oscar))
