import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, number: int):
        isAdmin = ctx.author.permissions_in(ctx.channel).administrator
        if (not isAdmin):
            await ctx.channel.send('You do not have sufficient privileges to access this command.')
            return
        deleted = await ctx.channel.purge(limit=number)
        await ctx.send(f'''Deleted __**{len(deleted)}**__ message(s)!''')

    @commands.command()
    async def kick(self, ctx, person: discord.Member):
        isAdmin = ctx.author.permissions_in(ctx.channel).administrator
        if (not isAdmin):
            await ctx.channel.send('You do not have sufficient privileges to access this command.')
            return
        await person.kick()
        await ctx.send('Good riddance!')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, messagestodelete: int=None):
        isAdmin = ctx.author.permissions_in(ctx.channel).administrator
        if (not isAdmin):
            await ctx.channel.send('You do not have sufficient privileges to access this command.')
            return
        if messagestodelete is not None:
            await member.ban(delete_message_days=messagestodelete)
        else:
            await member.ban()
        await ctx.send('It was about time you banned them.')

    @commands.command()
    async def unban(self, ctx, person: discord.User):
        isAdmin = ctx.author.permissions_in(ctx.channel).administrator
        if (not isAdmin):
            await ctx.channel.send('You do not have sufficient privileges to access this command.')
            return
        await ctx.guild.unban(person)
        await ctx.send(f'''Welcome back, {person.mention}!''')

    @commands.command()
    async def nick(self, ctx, member: discord.Member=None, *, newnick: str):
        if member is None:
            member = ctx.author
        isAdmin = ctx.author.permissions_in(ctx.channel).administrator
        if (not isAdmin):
            await ctx.channel.send('You do not have sufficient privileges to access this command.')
            return
        await member.edit(nick=newnick)
        await ctx.send(f'{member.mention} enjoy your new nickname!')


def setup(bot):
    bot.add_cog(Admin(bot))
