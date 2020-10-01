import discord
from discord.ext import commands
import random
from PIL import Image, ImageDraw, ImageFont
from json import load
from pyfiglet import figlet_format
import datetime
import aiohttp
import Levenshtein
import asyncio


class Fun(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sentences = load(open('configuration.json', 'r'))['sentences']

    @commands.command()
    async def duel(self, ctx, *, user: discord.Member=None):
        author = ctx.author
        if user is None:
            await ctx.send('At least mention someone to fight??')
        if user.id == self.bot.user.id:
            await ctx.send("I'm too good for you.")
        elif user.id == author.id:
            await ctx.send("You can't fight yourself, dumbass")
        else:
            await ctx.send(f'''{author.mention} and {user.mention} dueled for {str(random.randint(2, 120))} gruesome hours! It was a long, heated battle, but {random.choice([author.mention, user.mention])} emerged victorious!''')

    @commands.command()
    async def suck(self, ctx, *, thing: str=None):
        if thing is None:
            await ctx.send(f'''You suck {random.randint(1, 100)}%.''')
        elif thing == discord.Member:
            await ctx.send(f'''{thing.mention} sucks {random.randint(1, 100)}%.''')
        elif thing == '<@392907007444910083>':
            await ctx.send(f'''{thing.mention} doesn't suck at all.''')
        else:
            await ctx.send(f'''{thing} sucks {random.randint(1, 100)}%.''')

    @commands.command()
    async def flip(self, ctx):
        await ctx.send(f'''{ctx.author.mention}, choose either `heads` or `tails.`''')
        reply = await self.bot.wait_for('message')
        result = random.choice(['heads', 'tails'])
        if (result == 'heads') and reply.content.startswith('heads'):
            await ctx.send('You were right, it was heads! ;D')
        elif (result == 'heads') and reply.content.startswith('tails'):
            await ctx.send('It was heads, you lose! <:baha:452235896629100564>')
        elif (result == 'tails') and reply.content.startswith('tails'):
            await ctx.send('You were right, it was tails! ;D')
        elif (result == 'tails') and reply.content.startswith('heads'):
            await ctx.send('It was tails, you lose! <:baha:452235896629100564>')
        else:
            await ctx.send("You didn't pick heads or tails...")

    @commands.command()
    async def typeoff(self, ctx, player2: discord.Member=None):
        if player2 is None:
            randsent = random.choice(self.sentences)
            im = Image.open('blankpic.jpg')
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype('1942.ttf', 24)
            await ctx.send('Alright, you will have to type the sentence that shows up in 20 seconds.')
            draw.multiline_text((10, 25), randsent, fill=(0, 0, 0), font=font, spacing=5, align='left')
            im.save('newblankpic.jpg', quality=100)
            ttt = await ctx.channel.send(file=discord.File('newblankpic.jpg'))

            def check(m):
                return m.author == ctx.author

            try:
                reply = await self.bot.wait_for('message', check=check, timeout=20)
                newrandsent = ''.join(randsent.split('\n'))
                diff = reply.created_at - ttt.created_at
                scorecalc = Levenshtein.distance(reply.content, newrandsent)
                score = scorecalc*5
                await ctx.send(f'Yay, you did it! You get 5 points for each mistake you make, so your score was {score}! It took you {diff.total_seconds():.1f} seconds. \o/')
            except asyncio.TimeoutError:
                await ctx.send("You took too long, you lose!")
        else:
            randsent = random.choice(self.sentences)
            im = Image.open('blankpic.jpg')
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype('1942.ttf', 24)
            await ctx.send(f"Alright {ctx.author.mention}, you and {player2.mention} will have to type the sentence that shows up in under 20 seconds. Whoever sends it first, wins. If 20 seconds are up and no one finished, you both lose.")
            draw.multiline_text((10, 25), randsent, fill=(0, 0, 0), font=font, spacing=5, align='left')
            im.save('newblankpic.jpg', quality=100)
            ttt = await ctx.channel.send(file=discord.File('newblankpic.jpg'))

            def check(m):
                return m.author in [ctx.author, player2]

            try:
                reply = await self.bot.wait_for('message', check=check, timeout=20)
                newrandsent = ''.join(randsent.split('\n'))
                diff = reply.created_at - ttt.created_at
                if reply.author == player2:
                    score = Levenshtein.distance(reply.content, newrandsent)
                    score *= 5
                    await ctx.send(f"{player2.mention} wins! Their score was {score} and it took them {diff.total_seconds():.1f} seconds.")
                else:
                    score2 = Levenshtein.distance(reply.content, newrandsent)
                    score2 *= 5
                    await ctx.send(f"{ctx.author.mention} wins! Their score was {score2} and it took them {diff.total_seconds():.1f} seconds.")
            except asyncio.TimeoutError:
                await ctx.send("You guys took too long! You both lose.")

    @commands.command()
    async def ascii(self, ctx, *, txt):
        msg = str(figlet_format(txt, font='basic'))
        if msg[0] == ' ':
            msg = '.' + msg[1:]
        error = figlet_format('Your message is too long.', font='basic')
        if len(msg) > 2000:
            await ctx.send(f'''```{error}```''')
        else:
            await ctx.send(f'''```{msg}```''')

    @commands.command(aliases=['tih'])
    async def todayinhistory(self, ctx):
        d = datetime.date.today()
        month = d.month
        day = d.day
        url = f'''http://numbersapi.com/{month}/{day}/date?json'''
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                result = await r.json()
        embed = discord.Embed(title=result['text'], description=None)
        embed.color = 3749438
        await ctx.send(embed=embed)
        await cs.close()

    @commands.command()
    async def cat(self, ctx):
        url = "https://aws.random.cat/meow"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                result = await r.json()
        embed = discord.Embed(title="Cat", description=None)
        embed.set_image(url=result['file'])
        embed.color = 0x39363E
        await ctx.send(embed=embed)
        await cs.close()

    @commands.command()
    async def dog(self, ctx):
        url = "https://random.dog/woof.json"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                result = await r.json()
        embed = discord.Embed(title="Dog", description=None)
        embed.set_image(url=result['url'])
        embed.color = 0x39363E
        await ctx.send(embed=embed)
        await cs.close()

    @commands.command()
    async def spongebob(self, ctx, *, text: str):
        text = ''.join(random.choice([k.upper(), k]) for k in text)
        await ctx.send(text)


def setup(bot):
    bot.add_cog(Fun(bot))
