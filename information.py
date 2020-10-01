import discord
from discord.ext import commands
from datetime import datetime


class Information(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.launch_time = datetime.utcnow()

    @commands.command()
    async def ping(self, ctx):
        resp = await ctx.send("Pong! <a:pingmote:468026138938048525>")
        diff = resp.created_at - ctx.message.created_at
        await resp.edit(content=f'Pong! I took **{1000*diff.total_seconds():.1f}** miliseconds. >.>')

    @commands.group(name="help")
    async def _help(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='<:Opener:457451482002882562> <:leftdash:456800483441508359> Athena Control Center <:rightdash:456800544929873932>', description="**General**\n 〘`a!say`〙| Makes the bot say whatever you want. \n 〘`a!repeat <number of times> <message>`〙| Repeats your message \n 〘`a!choose <option1> <option2>`〙| Make the bot choose between multiple\n options. \n 〘`a!add <number> <number>`〙| Add two numbers together.\n 〘`a!suggest <suggestion>`〙| Suggest for commands to be added.\n**Information**\n 〘`a!uptime`〙| Tells you how long the bot has been online. \n 〘`a!ping`〙| Tells you the speed of the bot's connection to Discord. \n 〘`a!joined <@member>`〙| Tells you when a member joined the server.\n 〘`a!serverinfo`〙| Gives you information about the current server.\n 〘`a!userinfo <@user>`〙| Gives you information about the chosen user.\n 〘`a!about`〙| Tells you about Athena.\n**Fun**\n 〘`a!duel <@user>`〙| Have an old fashioned sword fight with another user.\n 〘`a!suck <thing or @user>`〙| Tells you how much something or someone sucks.\n 〘`a!flip`〙| Flip a coin and guess what it's going to be.\n**Overwatch**\n 〘`a!overwatch stats <battletag> <region>`〙| Shows player statistics in Overwatch.")
            embed.colour = 3553598
            embed.set_footer(text='For help on specific commands, run a!help <command>.')
            embed.timestamp = ctx.message.created_at
            await ctx.author.send(embed=embed)
            await ctx.send('DM sent.')

    @_help.command(name="say")
    async def _help_say(self, ctx):
        desc = '`a!say <message>`'
        embed = discord.Embed(title='Say command', description='**Description**\nMake the bot say whatever you want.')
        embed.add_field(name='Usage', value=desc)
        await ctx.send(embed=embed)

    @_help.command(name="ban")
    async def _help_ban(self, ctx):
        desc = '`a!ban <member> <optional-days of messages to delete>`'
        embed = discord.Embed(title="Ban command", description='**Description**\nBan a member from your server, also optional, delete x days worth of their messages.')
        embed.add_field(name='Usage', value=desc)
        await ctx.send(embed=embed)

    @_help.command(name="kick")
    async def _help_kick(self, ctx):
        desc = '`a!kick <member>`'
        embed = discord.Embed(title='Kick command', description='**Description**\nKick a member from your server.')
        embed.add_field(name='Usage', value=desc)
        await ctx.send(embed=embed)

    @_help.command(name='nick')
    async def _help_nick(self, ctx):
        desc = '`a!nick <member> <newnick>`'
        embed = discord.Embed(title='Nickname command', description="**Description**\nChange a member's nickname.")
        embed.add_field(name='Usage', value=desc)
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        (hours, remainder) = divmod(int(delta_uptime.total_seconds()), 3600)
        (minutes, seconds) = divmod(remainder, 60)
        (days, hours) = divmod(hours, 24)
        await ctx.send(f'''I have been up for {days} days, {hours} hours, {minutes} minutes and {seconds} seconds! ;D''')

    @commands.command()
    async def joined(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        await ctx.send('**{0.name}** joined on *{0.joined_at}*'.format(member))

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        members = set(guild.members)
        owner = guild.owner
        offline = filter((lambda m: (m.status is discord.Status.offline)), members)
        offline = set(offline)
        bots = filter((lambda m: m.bot), members)
        bots = set(bots)
        users = members - bots
        msg = '\n'.join(('**Name**                   : ' + guild.name, '**Date of creation**: ' + str(guild.created_at), '**Server Roles**      : %i' % (len(guild.roles) - 1), '**Server Owner**    : ' + ('{0.nick} ({0})'.format(owner) if owner.nick else str(owner)), '', '**Total Bots**        : %i' % len(bots), '**Bots Online**     : %i' % len(bots - offline), '**Bots Offline**    : %i' % len(bots & offline), '', '**Total Users**       : %i' % len(users), '**Users Online**    : %i' % len(users - offline), '**Users Offline**   : %i' % len(users & offline)))
        embed = discord.Embed(title=f'''Server info for {guild.name}''', description=msg)
        embed.colour = 3553598
        embed.set_thumbnail(url=guild.icon_url)
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text=f'''ID: {guild.id}''')
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member=None):
        author = ctx.author
        guild = ctx.guild
        if user is None:
            user = author
        roles = [x.name for x in user.roles if x.name != '@everyone']
        joined_at = self.fetch_joined_at(user, guild)
        since_created = (ctx.message.created_at - user.created_at).days
        since_joined = (ctx.message.created_at - joined_at).days
        user_joined = joined_at.strftime('%d %b %Y %H:%M')
        user_created = user.created_at.strftime('%d %b %Y %H:%M')
        created_on = '{}\n({} days ago)'.format(user_created, since_created)
        joined_on = '{}\n({} days ago)'.format(user_joined, since_joined)
        if roles:
            roles = sorted(roles, key=[x.name for x in guild.roles if x.name != '@everyone'].index)
            roles = ', '.join(roles)
        else:
            roles = 'None'
        embed = discord.Embed(title=f'''User info for {user}''', description=f'''Nick name(if existing): {user.nick}''')
        embed.add_field(name='__Roles__', value=roles)
        embed.add_field(name='__Joined Discord__', value=created_on)
        embed.add_field(name='__Joined server__', value=joined_on)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f'''User ID: {user.id}''')
        embed.colour = 3553598
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command()
    async def about(self, ctx):
        embedtitle = '<:leftdash:456800483441508359> About Athena <:rightdash:456800544929873932>'
        embed = discord.Embed(title=embedtitle, description='Athena is an in-dev multi-purpose Discord bot coded in Python by FallenSwords with help from some others. Credits to FlapJack for the overwatch stats command.\nSpecial credits to voldemort#6931 for teaching me the basics of starting a bot. u_u')
        embed.colour = 3553598
        embed.add_field(name='Created by', value='FallenSwords#8286')
        embed.add_field(name='Python version', value='Python 3.6.3')
        embed.add_field(name='Library', value=f'discord.py v{discord.__version__}')
        embed.add_field(name='Created on', value='20 Dec 2017')
        embed.add_field(name='Currently in', value=f'''{len(self.bot.guilds)} servers''')
        embed.set_footer(text=f'''Bot ID: {self.bot.user.id}''')
        embed.timestamp = ctx.message.created_at
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, person: discord.Member=None):
        if person is None:
            person = ctx.author
        embed = discord.Embed(title="Avatar")
        embed.set_author(name=person)
        embed.set_image(url=person.avatar_url)
        await ctx.send(embed=embed)

    def fetch_joined_at(self, user, guild):
        if (user.id == 96130341705637888) and (guild.id == 133049272517001216):
            return datetime.datetime(2016, 1, 10, 6, 8, 4, 443000)
        else:
            return user.joined_at


def setup(bot):
    bot.add_cog(Information(bot))
