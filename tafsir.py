from collections import OrderedDict
from aiohttp import ClientSession
from discord.ext import commands
from helpers import processRef
from utils import makeEmbed

icon = 'https://lh3.ggpht.com/zoyAL6BWpiHrgyFEujQcEXhBqZn4SfX0JiIFqOecs2JoZYy39Yam8xiz7Vq6kP7S2w=w300'


class TafsirError(Exception):
    pass


class TafsirSpecifics:
    def __init__(self, surah, ayah, maxayah):
        self.surah = surah
        self.minAyah = ayah
        self.maxAyah = maxayah
        self.tafsir = ''
        self.orderedDict = OrderedDict()

    def unpack(self):
        return self.surah, self.minAyah, self.maxAyah, self.tafsir, self.orderedDict


tafsir_list = ['jalalayn', 'muyassar']


class Tafsir:

    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession(loop=bot.loop)
        self.url = 'http://api.globalquran.com/ayah/{}:{}/{}'

    @commands.bot.command(pass_context=True)
    async def tafsir(self, ctx, ref: str, tafsir: str = None):

        # Debug info
        sender = ctx.message.author
        server = ctx.message.server
        serverid = ctx.message.server.id

        print(f'{sender} executed command tafsir on {server} ({serverid})')

        try:
            surah, min_ayah, max_ayah = processRef(ref)
            tafsirSpec = TafsirSpecifics(surah, min_ayah, max_ayah)
        except:
            await self.bot.say("Invalid arguments! Do `-tafsir [surah]:[ayah] (optional tafsir name)`. "
                               "Example: `-tafsir 1:1`"
                               "\n\n"
                               "To quote multiple verses, do `-tafsir [surah]:[first ayah]-[last ayah]`"
                               "\n\n"
                               "Example 2: `-tafsir 1:1-7 muyassar`"
                               "\n\n"
                               f"**Valid editions**: `{tafsir_list}`")
            return

        if tafsir is None:
            tafsir = 'ar.jalalayn'
            await self.bot.say('Defaulting to Tafsir al-Jalalayn.')
        else:
            try:
                tafsir = self.processTafsirName(tafsir)
            except TafsirError:
                await self.bot.say(f'Invalid tafsir. Valid tafsirs are: `{tafsir_list}`')
                return
        tafsirSpec.tafsir = tafsir

        await self.getTafsirs(tafsirSpec)
        readableTafsir = self.getReadableTafsirName(tafsir)

        em = makeEmbed(fields=tafsirSpec.orderedDict, author=readableTafsir, author_icon=icon, colour=0x467f05,
                       inline=False)

        await self.bot.say(embed=em)

    @staticmethod
    def processTafsirName(tafsir):
        if tafsir in tafsir_list:
            tafsir = 'ar.' + tafsir
        else:
            raise TafsirError

        return tafsir

    @staticmethod
    def getReadableTafsirName(tafsir):
        tafsirDict = {
            'ar.jalalayn': 'Tafsir al-Jalalayn',
            'ar.muyassar': 'Tafsir al-Muyassar',
        }
        return tafsirDict[tafsir]

    async def getTafsirs(self, tafsirspec):
        surah, minAyah, maxAyah, tafsir, orDict = tafsirspec.unpack()

        for verse in range(minAyah, maxAyah):
            await self.getTafsir(orDict, tafsir, surah, verse)

    async def getTafsir(self, orDict, tafsir, surah, verse):
        async with self.session.get(self.url.format(surah, verse, tafsir)) as r:
            data = await r.json()

        for page in data["quran"][f'{tafsir}'].values():

            text = page["verse"]
            surah = page["surah"]
            ayah = page["ayah"]

            text = u"{}".format(text)
            orDict[f'{surah}:{ayah}'] = text


# Register as cog
def setup(bot):
    bot.add_cog(Tafsir(bot))
