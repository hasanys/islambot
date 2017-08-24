import discord
from discord.ext import commands

description = 'A Discord bot which allows you to search ahadith from sunnah.com.'

bot = commands.Bot(command_prefix='.', description=description)

# Setup
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

    await bot.change_presence(game=discord.Game(name='-hadith to search ahadith'))

# Load cogs
bot.load_extension('hadith')
bot.load_extension('prayertimes')
bot.load_extension('quran')

bot.run('tokenhere')
