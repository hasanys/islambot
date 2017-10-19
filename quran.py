from aiohttp import ClientSession
from discord.ext import commands
from utils import makeEmbed
from helpers import processRef, Specifics
from main import prefix

icon = 'https://lh6.ggpht.com/hwhtsACU29Zv7NNKpLqH4k0NgCrdc6xU-B5PMx06PxH29PMz_PuBEFcmtvp37qZHhqGI=w300'
edition_list = ['sahih', 'ahmedali', 'ahmedraza', 'arberry', 'asad', 'daryabadi', 'hilali', 'pickthall', 'qaribullah',
                'sarwar', 'yusufali']


class QuranSpecifics(Specifics):
    def __init__(self, surah, minayah, maxayah, edition):
        super().__init__(surah, minayah, maxayah)
        self.edition = edition


class Quran:

    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession(loop=bot.loop)
        self.url = 'http://api.alquran.cloud/ayah/{}:{}/{}'

    @commands.bot.command()
    async def aquran(self, *, ref: str):

        try:
            quranSpec = self.getSpec(ref)
        except:
            await self.bot.say("Invalid arguments! Do `{0}aquran [surah]:[ayah]`. "
                               "Example: `{0}aquran 1:1`"
                               "\n"
                               "To quote multiple verses, do `{0}quran [surah]:[first ayah]-[last ayah]`"
                               "\n"
                               "Example: `{0}aquran 1:1-7`.".format(prefix))
            return

        try:
            surah_name = await self.getMetadata(quranSpec)
            await self.getVerses(quranSpec)

            em = makeEmbed(fields=quranSpec.orderedDict, author=surah_name, author_icon=icon, colour=0x78c741,
                           inline=False)
            await self.bot.say(embed=em)

        except:
            print(Exception)

    @commands.bot.command()
    async def quran(self, ref: str, edition: str = 'en.sahih'):

        if edition in edition_list:
            edition = 'en.' + edition
        elif edition != 'en.sahih':
            await self.bot.say(f'Invalid translation. Valid translation editions are: `{edition_list}`')

        try:
            quranSpec = self.getSpec(ref, edition = edition)
        except:
            await self.bot.say("Invalid arguments! Do `{0}quran [surah]:[ayah] (edition)`. "
                               "Example: `{0}quran 1:1`"
                               "\n"
                               "Example 2: `{0}quran 1:1 yusufali`"
                               "\n\n"
                               "To quote multiple verses, do `{0}quran [surah]:[first ayah]-[last ayah]`"
                               "\n"
                               "Example: `{0}quran 1:1-7`.".format(prefix))
            return

        try:

            surah_name, readableEdition = await self.getMetadata(quranSpec)
            await self.getVerses(quranSpec)

            em = makeEmbed(fields=quranSpec.orderedDict, author=f'Surah {surah_name} - {readableEdition}',
                           author_icon=icon, colour=0x78c741, inline=False)
            await self.bot.say(embed=em)

        except:
            print(Exception)

    @staticmethod
    def getSpec(ref, edition = 'ar'):
        surah, min_ayah, max_ayah = processRef(ref)
        return QuranSpecifics(surah, min_ayah, max_ayah, edition)

    async def getVerses(self, spec):
        for verse in range(spec.minAyah, spec.maxAyah):
            async with self.session.get(self.url.format(spec.surah, verse, spec.edition)) as r:
                data = await r.json()

            spec.orderedDict['{}:{}'.format(spec.surah, verse)] = data['data']['text']

    async def getMetadata(self, spec):
        async with self.session.get(self.url.format(spec.surah, spec.minAyah, spec.edition)) as r:
            data = await r.json()
        if spec.edition == 'ar':
            return data['data']['surah']['name']
        else:
            return data['data']['surah']['englishName'], data['data']['edition']['name']


# Register as cog
def setup(bot):
    bot.add_cog(Quran(bot))
