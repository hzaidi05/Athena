import traceback
import sys
from discord.ext import commands


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send(f'{error.param.name} is a required argument that is missing.')

        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"I could not find that command. If you would like it to be one, suggest it with `a!suggest <suggestion>`")

        elif isinstance(error, commands.TooManyArguments):
            return await ctx.send("You're providing too many arguments!")

        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"You do not have enough permissions to use this command.")

        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send("I don't have enough permissions!")

        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')

        elif isinstance(error, commands.BadArgument):
            return await ctx.send('Bad argument, please try again.')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
