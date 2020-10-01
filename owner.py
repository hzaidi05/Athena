import discord
import io
import textwrap
import traceback
from contextlib import redirect_stdout
from discord.ext import commands
import datetime


class Owner(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_result = None
        self.owner = bot.get_user(341295279674228737)
        self.startup_extensions = ['overwatch', 'information', 'general', 'fun', 'admin', 'owner']

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

    @commands.group(name='activity')
    async def activity(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('You forgot listening playing watching etc whatever')

    @activity.command()
    async def playing(self, ctx, *, vgame: str):
        if ctx.author != self.owner:
            return
        await self.bot.change_presence(activity=discord.Game(name=vgame))
        await ctx.send('Done.')

    @activity.command()
    async def listening(self, ctx, *, thing: str):
        if ctx.author != self.owner:
            return
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=thing))
        await ctx.send('Done.')

    @activity.command()
    async def watching(self, ctx, *, movie: str):
        if ctx.author != self.owner:
            return
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=movie))
        await ctx.send('Done.')

    @commands.command()
    async def annoy(self, ctx, annoyee: discord.Member):
        msg = ctx.message
        await msg.delete()
        ping = await ctx.send(f'''{annoyee.mention}, you're such a noob.''')
        await ping.delete()

    @commands.command()
    async def editusr(self, ctx, newusr: str):
        await self.bot.user.edit(username=newusr)
        await ctx.send("Done.")

    @commands.command(name="eval")
    async def _eval(self, ctx, *, body: str):
        if ctx.author == self.owner:
            env = {
                'bot': self.bot,
                'ctx': ctx,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                '_': self._last_result
            }

            env.update(globals())

            body = self.cleanup_code(body)
            stdout = io.StringIO()

            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

            try:
                exec(to_compile, env)
            except Exception as e:
                return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                await ctx.message.add_reaction('\u2705')

                if ret is None:
                    if value:
                        await ctx.send(f'```py\n{value}\n```')
                else:
                    self._last_result = ret
                    await ctx.send(f'```py\n{value}{ret}\n```')
        else:
            return

    @commands.command()
    async def shutdown(self, ctx):
        if ctx.author != self.owner:
            return
        await ctx.send('Shutting down... ')
        await self.bot.logout()
        await self.bot.close()

    @commands.command()
    async def broadcast(self, ctx, *, body: str):
        if ctx.author != self.owner:
            return
        for guild in self.bot.guilds:
            incharge = guild.owner
            await incharge.send(content=body)
        await ctx.send("Done")

    @commands.command()
    async def cogreload(self, ctx, extension_name: str):
        self.bot.reload_extension(extension_name)
        await ctx.send(f"{extension_name} reloaded.")


def setup(bot):
    bot.add_cog(Owner(bot))
