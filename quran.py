from collections import OrderedDict
from aiohttp import ClientSession
from discord.ext import commands
from utils import makeEmbed
from helpers import processRef

icon = 'https://lh6.ggpht.com/hwhtsACU29Zv7NNKpLqH4k0NgCrdc6xU-B5PMx06PxH29PMz_PuBEFcmtvp37qZHhqGI=w300'
edition_list = ['sahih', 'ahmedali', 'ahmedraza', 'arberry', 'asad', 'daryabadi', 'hilali', 'pickthall', 'qaribullah',
                'sarwar', 'yusufali']


class Quran:

    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession(loop=bot.loop)

    @commands.bot.command(pass_context=True)
    async def aquran(self, ctx, *, ref: str):

        try:
            surah, min_ayah, max_ayah = processRef(ref)
        except:
            await self.bot.say("Invalid arguments! Do `.aquran [surah]:[ayah]`. Example: `.aquran 1:1`\nTo quote multi"
                               "ple verses, do `.quran [surah]:[first ayah]-[last ayah]`\nExample: `.aquran 1:1-7`.")
            return

        try:

            # Text needs to be in an OrderedDict for some reason
            o = OrderedDict()

            # Set base URL
            url = 'http://api.alquran.cloud/ayah/{}:{}/ar'

            # Get data from API
            async with self.session.get(url.format(surah, min_ayah)) as r:
                data = await r.json()

            # Get variables and text
            surah_name =  data['data']['surah']['name']
            o['{}:{}'.format(surah, min_ayah)] = data['data']['text']

            # If multiple ayahs need to be quoted, get the text for them
            for verse in range(min_ayah + 1, max_ayah):
                async with self.session.get(url.format(surah, verse)) as r:
                    data = await r.json()
                o['{}:{}'.format(surah, verse)] = data['data']['text']

            # Construct and send the embed
            em = makeEmbed(fields=o, author=surah_name, author_icon=icon, colour=0x78c741,
                           inline=False)
            await self.bot.say(embed=em)

        except:
            print(Exception)

    # English Quran

    @commands.bot.command(pass_context=True)
    async def quran(self, ctx, ref: str, edition: str = None):

        # Get surah
        try:
            surah, min_ayah, max_ayah = processRef(ref)
        except:
            await self.bot.say("Invalid arguments! Do `.quran [surah]:[ayah] (edition)`. Example: `.quran 1:1`\n"
                               "Example 2: `.quran 1:1 yusufali`\n\nTo quote multiple verses, do `.quran [surah]:[first"
                               " ayah]-[last ayah]`\nExample: `.quran 1:1-7`.")
            return

        # Default to Sahih International if no edition is specified
        if edition is None:
            edition = 'en.sahih'

        # Valid edition? Just add 'en.' before the edition name to convert it to the name needed for API
        elif edition in edition_list:
            edition = 'en.' + edition

        # Otherwise, give the invalid edition error message.
        else:
            await self.bot.say(f'Invalid translation. Valid translation editions are: `{edition_list}`')

        try:

            # Text needs to be in an OrderedDict for some reason
            o = OrderedDict()

            # Set base URL
            url = 'http://api.alquran.cloud/ayah/{}:{}/{}'

            # Get data from API
            async with self.session.get(url.format(surah, min_ayah, edition)) as r:
                data = await r.json()

            # Get variables and text
            surah_name = data['data']['surah']['englishName']
            o['{}:{}'.format(surah, min_ayah)] = data['data']['text']

            # If multiple ayahs need to be quoted, get the text for them
            for verse in range(min_ayah + 1, max_ayah):
                async with self.session.get(url.format(surah, verse, edition)) as r:
                    data = await r.json()
                o['{}:{}'.format(surah, verse)] = data['data']['text']

            # Get the edition name in English
            edition = data['data']['edition']['name']

            # Construct and send the embed
            em = makeEmbed(fields=o, author=f'Surah {surah_name} - {edition}', author_icon=icon, colour=0x78c741,
                           inline=False)
            await self.bot.say(embed=em)

        except:
            print(Exception)


# Register as cog
def setup(bot):
    bot.add_cog(Quran(bot))
