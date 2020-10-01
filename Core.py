from json import load
import discord
from discord.ext import commands

startup_extensions = ['overwatch', 'information', 'general', 'fun', 'admin', 'owner', 'errorhandler']

bot = commands.Bot(command_prefix=['a!', '<@392907007444910083> ', 'Athena, '])
owner = 341295279674228737
bot.remove_command("help")


@bot.event
async def on_ready():
    print('𝔸𝕥𝕙𝕖𝕟𝕒')
    print('------')
    print('Connected to Discord.')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='Overwatch', type=0))


@bot.command()
async def cogload(ctx, extension_name: str):
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send('```py\n{}: {}\n```'.format(type(e).__name__, str(e)))
        return
    await ctx.send('{} loaded.'.format(extension_name))


@bot.command()
async def cogunload(ctx, extension_name: str):
    bot.unload_extension(extension_name)
    await ctx.send('{} unloaded.'.format(extension_name))


@bot.event
async def on_message(message):
    if message.content.startswith('AA'):
        await message.channel.send(file=discord.File('AA.gif'))
    if message.content.startswith('REE'):
        await message.channel.send(file=discord.File('REE.gif'))
    if "dwarf" in message.content:
        await message.channel.send("I'm not a dwarf, I'm Swedish!")
    await bot.process_commands(message)


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(load(open('configuration.json', 'r'))['token'])
