import discord
from discord.ext import commands
import numbers
import aiohttp


class Overwatch(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.base_url = 'https://us.battle.net/connect/en/app/'
        self.product_url = '/patch-notes?productType='
        self.patch_url = {
            'overwatch': 'https://playoverwatch.com/en-us/game/patch-notes/pc/',
        }
        self.thumb = {
            'overwatch': 'https://i.imgur.com/YZ4w2ey.png',
        }
        self.header = {
            'User-Agent': 'OverwatchCog/1.0',
        }
        self.patch_header = {
            'User-Agent': 'Battle.net/1.0.8.4217',
        }
        self.emoji = {
            'next': '➡',
            'back': '⬅',
            'no': '❌',
        }

    def dictgrab(self, my_dict, *keys):
        temp_dict = my_dict
        for key in keys:
            temp_dict = temp_dict.get(key)
            if temp_dict is None:
                return '-'
        if isinstance(temp_dict, numbers.Number):
            return str(round(temp_dict))
        else:
            return '-'

    @commands.group(name='overwatch', aliases=['ow'])
    async def overwatch(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('You have not used any subcommand! \nFor help on the Overwatch category, do `a!help overwatch`.')

    @overwatch.command(name='stats')
    async def _overwatch_stats(self, ctx, tag: str=None, region: str=None):
        if (tag in ['kr', 'eu', 'us']) and (region is None):
            region = tag
            tag = None
        if tag is None:
            await ctx.send("You haven't entered a battle tag!")
            return
        tag = tag.replace('#', '-')
        url = ('https://owapi.net/api/v3/u/' + tag) + '/stats'
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url, headers=self.header) as response:
                stats = await response.json()
        if 'error' in stats:
            await ctx.send('Could not fetch your statistics. Battle tags are case sensitive and requie a 4 or 5 digit identifier. Example: Username#1234')
            return
        if region is None:
            if stats['kr']:
                region = 'kr'
            elif stats['eu']:
                region = 'eu'
            elif stats['us']:
                region = 'us'
            else:
                await ctx.send('That battletag has no stats in any region.')
                return
        region_full = self.ow_full_region(region)
        if (region not in stats.keys()) or (stats[region] is None):
            await ctx.send('That battle tag exists but I could not find stats for it in the region specified. Use `eu`, `us` or `kr`.')
            return
        url = (('https://playoverwatch.com/en-us/career/pc/' + region) + '/') + tag
        tag = tag.replace('-', '#')
        qplay = stats[region]['stats']['quickplay']
        if qplay is None:
            qplay_stats = '*No matches played*'
            thumb_url = self.thumb['overwatch']
        else:
            thumb_url = qplay['overall_stats']['avatar']
            qplay_stats = ''.join(['**Wins:** ', self.dictgrab(qplay, 'game_stats', 'games_won'), '\n**Avg Elim:** ', self.dictgrab(qplay, 'average_stats', 'eliminations_avg'), '\n**Avg Death:** ', self.dictgrab(qplay, 'average_stats', 'deaths_avg'), '\n**Avg Heal:** ', self.dictgrab(qplay, 'average_stats', 'healing_done_avg')])
        comp = stats[region]['stats']['competitive']
        footer = None
        if comp is None:
            comp_stats = '*No matches played*'
            tier = None
        elif comp['overall_stats']['comprank'] is None:
            comp_stats = '*Not ranked*'
            tier = None
        else:
            tier = comp['overall_stats']['tier']
            footer = 'SR: ' + str(comp['overall_stats']['comprank'])
            comp_stats = ''.join(['**Wins:** ', self.dictgrab(comp, 'game_stats', 'games_won'), '\n**Avg Elim:** ', self.dictgrab(comp, 'average_stats', 'eliminations_avg'), '\n**Avg Death:** ', self.dictgrab(comp, 'average_stats', 'deaths_avg'), '\n**Avg Heal:** ', self.dictgrab(comp, 'average_stats', 'healing_done_avg')])
        icon_url = self.ow_tier_icon(tier)
        embed = discord.Embed(title=('Overwatch Stats (PC-' + region_full) + ')', color=16425006)
        embed.set_author(name=tag, url=url, icon_url=icon_url)
        embed.set_thumbnail(url=thumb_url)
        embed.add_field(name='__Competitive__', value=comp_stats, inline=True)
        embed.add_field(name='__Quick Play__', value=qplay_stats, inline=True)
        if footer is not None:
            embed.set_footer(text=footer)
        await ctx.send(embed=embed)
        await cs.close()

    def ow_tier_icon(self, tier: str):
        return {
            'bronze': 'https://i.imgur.com/B4IR72H.png',
            'silver': 'https://i.imgur.com/1mOpjRc.png',
            'gold': 'https://i.imgur.com/lCTsNwo.png',
            'platinum': 'https://i.imgur.com/nDVHAbp.png',
            'diamond': 'https://i.imgur.com/fLmIC70.png',
            'master': 'https://i.imgur.com/wjf0lEc.png',
            'grandmaster': 'https://i.imgur.com/5ApGiZs.png',
        }.get(tier, self.thumb['overwatch'])

    def ow_full_region(self, region: str):
        return {
            'kr': 'Asia',
            'eu': 'Europe',
            'us': 'US',
        }.get(region, ' ')

    @commands.group(name='overwatchlore', aliases=['owlore'])
    async def overwatchlore(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('You have not invoked a subcommand!\nUse a!help overwatchlore for help on this set of commands.')

    @overwatchlore.command(name='tag')
    async def _overwatchlore_tag(self, ctx, tag: str=None):
        if tag is None:
            await ctx.send("You haven't entered a tag!")
        await ctx.send('Alright, fetching a post for you.')
        tag = tag.replace('+', ' ')
        url = f'''https://api.tumblr.com/v2/blog/obscurewatch.tumblr.com/posts/text?api_key=Yfp0qf5wUIxYZKCqIB7BZ83uhjxg4F8UtbqSRbN1LCZf02XOmK&tag={tag}'''
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                thepost = await r.json()
        print(thepost['response']['posts'][18])

    @commands.group(name="comic", aliases=['c'])
    async def comic(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You haven't specificed a comic!")

    @comic.command(name="train-hopper")
    async def train_hopper(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/mccree-train-hopper")

    @comic.command(name="dragon-slayer")
    async def dragon_slayer(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/reinhardt-dragon-slayer")

    @comic.command(name="going-legit")
    async def going_legit(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/junkrat-roadhog-going-legit")

    @comic.command(name="a-better-world")
    async def better_world(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/symmetra-a-better-world")

    @comic.command(name="mission-statement")
    async def mission_statement(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/pharah-mission-statement")

    @comic.command(name="destroyer")
    async def destroyer(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/torbjorn-destroyer")

    @comic.command(name="legacy")
    async def legacy(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/legacy")

    @comic.command(name="old-soldiers")
    async def old_soldiers(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/ana-old-soldiers")

    @comic.command(name="junkenstein")
    async def junkenstein(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/junkrat-junkenstein")

    @comic.command(name="reflections")
    async def reflections(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/tracer-reflections")

    @comic.command(name="binary")
    async def binary(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/bastion-binary")

    @comic.command(name="uprising")
    async def uprising(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/tracer-uprising")

    @comic.command(name="masquerade")
    async def masquerade(self, ctx):
        await ctx.send("https://comic.playoverwatch.com/en-us/doomfist-masquerade")

    @comic.command(name="wasted-land")
    async def wasted_land(self, ctx):
        await ctx.send("https://comic.playoverwatch.com/en-us/junkertown-wasted-land")

    @comic.command(name="searching")
    async def searching(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/zarya-searching")

    @comic.command(name="halloween-terror")
    async def halloween_terror(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/junkrat-the-return-of-junkenstein")

    @comic.command(name="yeti-hunt")
    async def yeti_hunt(self, ctx):
        await ctx.send("http://comic.playoverwatch.com/en-us/yeti-hunt")

    @comic.command(name="retribution")
    async def retribution(self, ctx):
        await ctx.send("https://bit.ly/2JiNaZq")

    @commands.group(name="bio")
    async def bio(self, ctx, hero: str=None):
        if hero is None:
            await ctx.send("You haven't specified which hero's bio you want to see.")


def setup(bot):
    bot.add_cog(Overwatch(bot))
