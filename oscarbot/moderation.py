import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime, timedelta
import time
from .utils import times, separate, Timer
import os
import sqlite3

class Moderation(commands.Cog):
    def __init__(self, oscar):
        self.oscar = oscar

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member, *reason):
        # Bans a specified member from the guild. A reason is optional.
        reason = " ".join(reason)
        await member.ban(reason=reason)

        embed = discord.Embed(title="Member banned", timestamp=datetime.now(), color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Ban", icon_url="attachment://logo.png")
        embed.add_field(name="{0} has timedelta been banned by {1} for {2}".format(member, ctx.message.author, reason), value="** **")
        embed.set_footer(text=f'ID: {member.id}')
        await ctx.send(file=logo,embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        # Unbans a user from the guild.
        banned_users = await ctx.guild.bans()
        member_name = str(member[:-5])
        member_discriminator = str(member[-4:])

        for ban in banned_users:
            user = ban.user
            if (member_name, member_discriminator) == (user.name, user.discriminator):
                await ctx.guild.unban(user)

                embed = discord.Embed(title="Member unbanned",timestamp=datetime.now(),color=discord.Colour.darker_grey())
                logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
                embed.set_author(name="Unban", icon_url="attachment://logo.png")
                embed.add_field(name="{0} has been unbanned.".format(member), value="** **")
                await ctx.send(file=logo, embed=embed)
                  
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member, *reason):
        # Kicks a specified member from the guild. A reason is optional.
        await member.kick()

        embed = discord.Embed(title="Member kicked",timestamp=datetime.now(),color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Kick", icon_url="attachment://logo.png")
        embed.add_field(name="{0} has been kicked by {1} for {2}".format(member, ctx.message.author, " ".join(reason)), value="** **")
        embed.set_footer(text=f'ID: {member.id}')
        await ctx.send(file=logo,embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member:discord.Member, *args):
        # Adds a muted role to a member. Creates the role if it does not exist.
        # Optional time and reason parameters
        if get(ctx.guild.roles, name="Muted") in member.roles:
            await ctx.send("That member is already muted.")

        else:
            if args:
                time, reason = separate(args)
            else:
                time, reason = "indefinitely.", "no reason specified."

            perms = discord.Permissions(view_channel=True, read_message_history=True)
            if not get(ctx.guild.roles, name="Muted"):
                # Creates the role if it doesnt not exist
                await ctx.guild.create_role(name="Muted", hoist=True, permissions=perms)

            muted_role = get(ctx.guild.roles, name="Muted")
            await member.add_roles(muted_role)

            for guild in self.oscar.guilds:
                for tc in guild.text_channels:
                    await tc.set_permissions(muted_role, send_messages=False, add_reactions=False)
                for vc in guild.voice_channels:
                    await vc.set_permissions(muted_role, connect=False)

            embed = discord.Embed(title=f"{member} muted", timestamp=datetime.now(), color=discord.Colour.darker_grey())
            logo = discord.File("/Oscar Bot/logo.png", filename="logo.png")
            embed.set_author(name="Mute", icon_url="attachment://logo.png")
            embed.add_field(name="Time", value=f"{time}")
            embed.add_field(name="Reason", value=f"{reason}")
            embed.set_footer(text=f'ID: {member.id}')
            await ctx.send(file=logo, embed=embed)

            if time != "indefinitely.":
                timer = Timer()
                timer.start(time)
                while True:
                    if Timer.elapsed_time == None:
                        await member.remove_roles(muted_role)
                        break

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member):
        muted_role = get(member.guild.roles, name="Muted")

        if muted_role not in member.roles:
            await ctx.send("That member is not muted.")

        else:
            muted_role = get(member.guild.roles, name="Muted")
            await member.remove_roles(muted_role)

            embed = discord.Embed(title="Member unmuted",timestamp=datetime.now(),color=discord.Colour.darker_grey())
            logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
            embed.set_author(name="Unmute", icon_url="attachment://logo.png")
            embed.add_field(name="{0} has been unmuted.".format(member), value="** **")
            embed.set_footer(text=f'ID: {member.id}')
            await ctx.send(file=logo,embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def warn(self, ctx, member:discord.Member, *reason):
        reason = " ".join(reason)
        if not reason:
            reason = "no reason specified."
 
        conn = sqlite3.connect(os.path.realpath("../Oscar Bot/warnslist.db"))
        cursor = conn.cursor()
        n = cursor.execute("SELECT total FROM warns WHERE member = (?)", (str(member),)).fetchall()
        cursor.execute("INSERT INTO warns (member, reasons, total) values (?, ?, ?)", (str(member), reason, len(n)+1))
        conn.commit()
        conn.close()

        embed = discord.Embed(title="Member warned",timestamp=datetime.now(),color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Warn", icon_url="attachment://logo.png")
        embed.add_field(name="{0} has been warned. They now have {1} warns.".format(member, len(n)+1), value="** **")
        embed.add_field(name="Reason: {0}".format(reason), value="** **", inline=False)
        embed.set_footer(text=f'ID: {member.id}')
        await ctx.send(file=logo,embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def clearwarns(self, ctx, member:discord.Member, *amount:int):
        # Clears a specified amount of warns for a member. Clears all if none specified
        conn = sqlite3.connect(os.path.realpath("../Oscar Bot/warnslist.db"))
        cursor = conn.cursor()
        cursor.execute('DELETE FROM warns WHERE member = (?)', (str(member),))
        conn.commit()
        cursor.close

        embed = discord.Embed(title="Warns cleared for {0}".format(str(member)),timestamp=datetime.now(),color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Clear warns", icon_url="attachment://logo.png")
        embed.set_footer(text=f'ID: {member.id}')
        await ctx.send(file=logo,embed=embed)

    @commands.command()
    async def warnlist(self, ctx, member:discord.Member):
        # Returns a list of warns and reasons for a specified member
        conn = sqlite3.connect(os.path.realpath("../Oscar Bot/warnslist.db"))
        cursor = conn.cursor()

        t = cursor.execute("SELECT total FROM warns WHERE member = (?)", (str(member),)).fetchall()
        r = cursor.execute("SELECT reasons FROM warns WHERE member = (?)", (str(member),)).fetchall()
        r = [i[0] for i in r]

        embed = discord.Embed(title="Warns for {0}".format(member), timestamp=datetime.now(), color=discord.Colour.darker_grey())
        logo = discord.File("../Oscar Bot/logo.png", filename="logo.png")
        embed.set_author(name="Warnlist", icon_url="attachment://logo.png")
        embed.add_field(name="Total: {0}".format(len(t)), value="** **", inline=False)
        for n in range(len(r)):
            embed.add_field(name="Warn {0}".format(n+1), value="{0}".format(r[n]))

        embed.set_footer(text=f'ID: {member.id}')
        await ctx.send(file=logo,embed=embed)

def setup(oscar):
    oscar.add_cog(Moderation(oscar))
