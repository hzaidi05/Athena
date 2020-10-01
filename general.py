import discord
from discord.ext import commands
import random
from discord.ext.commands.cooldowns import BucketType
import asyncio


class General(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, text: str):
        message = ctx.message
        await message.delete()
        await ctx.send(text)

    @commands.command()
    @commands.cooldown(1, 15, BucketType.user)
    async def repeat(self, ctx, times: int, *, content='Repeating...'):
        if times > 25:
            await ctx.send("I can't repeat that many times, I might choke!")
            return
        for i in range(times):
            await ctx.send(content)

    @repeat.error
    async def repeat_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            seconds - round(seconds, 2)
            (hours, remainder) = divmod(int(seconds), 3600)
            (minutes, seconds) = divmod(remainder, 60)
            await ctx.send(f'''You are on cooldown; {minutes}m and {seconds}s remaining.''')

    @commands.command()
    async def choose(self, ctx, *choices: str):
        await ctx.send(random.choice(choices))

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        await ctx.send(left + right)

    @commands.command()
    async def suggest(self, ctx, *, suggestion: str=None):
        owner = self.bot.get_user(341295279674228737)
        if suggestion is None:
            await ctx.send("You haven't even given a suggestion?")
        else:
            embed = discord.Embed(title=f'''Suggestion from {ctx.author}''', description=suggestion)
            embed.colour = 3553598
            await owner.send(embed=embed)
            await ctx.send('Suggestion sent.')

    @commands.command(aliases=['remindme', 'reminder'])
    async def remind(self, ctx, quantity: int, timeunit: str, *, toremind: str):
        author = ctx.author
        if timeunit == "m":
            timetosleep = quantity*60
        elif timeunit == "h":
            timetosleep = quantity*3600
        elif timeunit == "d":
            timetosleep = quantity*86400
        elif timeunit == "w":
            timetosleep = quantity*604800
        elif timeunit == "s":
            timetosleep = quantity
        await ctx.send(f"Alright {author.mention}, I'll remind you about `{toremind}` in {quantity} {timeunit}!")
        await asyncio.sleep(timetosleep)
        await ctx.send(f"{author.mention}, I was told told to remind you about `{toremind}`.")


def setup(bot):
    bot.add_cog(General(bot))
