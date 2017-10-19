from collections import OrderedDict
from aiohttp import ClientSession
from discord.ext import commands
from utils import makeEmbed

icon = 'https://lh3.ggpht.com/zoyAL6BWpiHrgyFEujQcEXhBqZn4SfX0JiIFqOecs2JoZYy39Yam8xiz7Vq6kP7S2w=w300'

tafsir_list = ['jalalayn', 'muyassar']
class Tafsir:

    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession(loop=bot.loop)

    @commands.bot.command(pass_context=True)
    async def tafsir(self, ctx, ref: str, tafsir: str = None):

        # Debug info
        sender = ctx.message.author
        server = ctx.message.server
        serverid = ctx.message.server.id
        print(f'{sender} executed command tafsir on {server} ({serverid})')

        # Get surah
        surah = int(ref.split(':')[0])

        # Get first ayah
        min_ayah = int(ref.split(':')[1].split('-')[0])

        # Get last ayah
        try:
            max_ayah = int(ref.split(':')[1].split('-')[1]) + 1
        except IndexError:
            max_ayah = min_ayah + 1

        # Otherwise throw an error
        except:
            await self.bot.say("Invalid arguments! Do `-tafsir [surah]:[ayah] (optional tafsir name)`. Example: `-tafsi"
                               "r 1:1`\n\nTo quote multiple verses, do `-tafsir [surah]:[first ayah]-[last ayah]`\n\nEx"
                               "ample 2: `-tafsir 1:1-7 muyassar`"
                               f"\n\n**Valid editions**: `{tafsir_list}`")
            return

        # No tafsir specified? Default to Tafsir al-Jalalayn
        if tafsir is None:
            tafsir = 'ar.jalalayn'
            await self.bot.say('Defaulting to Tafsir al-Jalalayn.')

        # Valid tafsir? Just add 'ar.' before the edition name to convert it to the name needed for API
        elif tafsir in tafsir_list:
            tafsir = 'ar.' + tafsir

        # Otherwise, give the invalid edition error message.
        else:
            await self.bot.say(f'Invalid tafsir. Valid tafsirs are: `{tafsir_list}`')
            return

        # Text needs to be in an OrderedDict for some reason
        o = OrderedDict()

        # Set base URL
        url = 'http://api.globalquran.com/ayah/{}:{}/{}'

        # Get data from API
        async with self.session.get(url.format(surah, min_ayah, tafsir)) as r:
            data = await r.json()

        # Get tafsir text

        # Stage 1: Load the JSON and list values
        for page in data["quran"][f'{tafsir}'].values():

            # Stage 2: Search for the 'verse' key and assign it to the text variable
            text = page["verse"]

            '''
            If we input an invalid ayah number for surah (e.g 1:1000), it will just carry onto the next
            surahs, so in case this happens, get the actual surah and ayah number from the page.
            '''

            surah = page["surah"]
            ayah = page["ayah"]

            # Stage 3: Convert from unicode numbers to characters we can read
            text = u"{}".format(text)
            o[f'{surah}:{ayah}'] = text

        # If multiple ayahs need to be quoted, get the tafsir text for them
        for verse in range(min_ayah + 1, max_ayah):
            async with self.session.get(url.format(surah, verse, tafsir)) as r:
                data = await r.json()

                # Get tafsir text (as above)
                for page in data["quran"][f'{tafsir}'].values():
                    text = page["verse"]
                    text = u"{}".format(text)

                    surah = page["surah"]
                    ayah = page["ayah"]
                    o['{}:{}'.format(surah, verse)] = text

        # Format tafsir name
        tafsir = {
            'ar.jalalayn': 'Tafsir al-Jalalayn',
            'ar.muyassar': 'Tafsir al-Muyassar',
        }[tafsir]

        # Construct and send the embed
        em = makeEmbed(fields=o, author=tafsir, author_icon=icon, colour=0x467f05,
                       inline=False)
        await self.bot.say(embed=em)


# Register as cog
def setup(bot):
    bot.add_cog(Tafsir(bot))
