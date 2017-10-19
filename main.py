import discord
from helpers import prefix
from discord.ext import commands

description = "A bot with Qu'ran, hadith, hijri calendar and prayer time functions. Bot owner: @Zaify#6850"
bot = commands.Bot(command_prefix=prefix, description=description)
servers = len(bot.servers)


# Setup
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(game=discord.Game(name=f'-help on {servers} servers'))


# Load cogs
cog_list = ['hadith', 'prayertimes', 'quran', 'hijricalendar', 'tafsir']
for cog in cog_list:
    bot.load_extension(cog)


# Reload cog command for owner
@bot.command(pass_context=True, hidden=True)
async def reload(ctx):
    if ctx.message.author.id == '184402067685638144':
        for cog in cog_list:
            bot.unload_extension(cog)
            print(f'Unloading {cog}')
        for cog in cog_list:
            bot.load_extension(cog)
            print(f'Loading {cog}')
        await bot.say('Reload complete!')
    else:
        await bot.say('Only @Zaify#6850 can reload the bot.')

bot.run('tokenhere')
