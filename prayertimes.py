import discord
from aiohttp import ClientSession
from discord.ext import commands

icon = 'http://cdn.mysitemyway.com/icons-watermarks/flat-circle-white-on-green/ocha/ocha_infrastructure-mosque/ocha_i' \
       'nfrastructure-mosque_flat-circle-white-on-green_512x512.png'

method_list = ['1', '2', '3', '4', '5']
maddhab_list = ['hanafi', 'shafii']


class PrayerTimes:

    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession(loop = bot.loop)
        self.url = 'http://api.aladhan.com/timingsByAddress?address={location}&method={method}&school={maddhab}'

    @commands.bot.command()
    async def prayertimes(self, location: str, method: str = None, maddhab: str = None):

        if method is not None and method not in method_list:
                await self.bot.say('The method must be a number between 1 and 5.```'
                                   '\n1 = University of Islamic Sciences, Karachi'
                                   '\n2 = Islamic Society of North America (ISNA)'
                                   '\n3 = Muslim World League (MWL)'
                                   '\n4 = Umm al-Qura, Makkah'
                                   '\n5 = Egyptian General Authority of Survey```')
                return

        elif method is None:
            await self.bot.say('*No method specified. Defaulting to Umm al-Qura, Makkah.*')
            method = '4'

        if maddhab is not None:
            maddhab = maddhab.lower()

        # Now process the maddhab - if maddhab is valid then convert to integers needed for URL:
        maddhab, sayStr = self.getMaddhab(maddhab)
        if sayStr:
            await self.bot.say(sayStr)

        try:
            text = await self.getPrayerTimes(location, method, maddhab)

            # Convert method integers into the actual names
            method = self.getReadableMethodName(method)

            # Convert back to maddhab names
            maddhab = self.getReadableMaddhabName(maddhab)

            # Construct and send embed
            em = discord.Embed(title=f"{method} - {maddhab}", description=text, colour=0x78c741)
            em.set_author(name=f'Salat Times for {location}', icon_url=icon)
            await self.bot.say(embed=em)

        except:
            await self.bot.say('Invalid arguments! Usage: `.prayertimes [location] [method] [maddhab]`.\n'
                               'Example: `.prayertimes London 4 Shafii`\n'
                               'You can include multiple words in the location by enclosing it in quotes. Example:'
                               '`.prayertimes "East London Mosque" 4 Shafii`')

    def getReadableMaddhabName(self, maddhab):
        maddhabDict = {
                '0': "Shafi'i",
                '1': 'Hanafi',
            }
        return maddhabDict[maddhab]

    def getReadableMethodName(self, method):
        methodDict = {
            '1': 'University of Islamic Sciences, Karachi',
            '2': 'Islamic Society of North America (ISNA)',
            '3': 'Muslim World League (MWL)',
            '4': 'Umm al-Qura, Makkah',
            '5': 'Egyptian General Authority of Survey',
        }
        return methodDict[method]

    async def getPrayerTimes(self, location, method, maddhab):
        async with self.session.get(self.url.format(location, method, maddhab)) as r:
            data = r.json()

        timings = data['data']['timings']

        # Assign variables from JSON
        fajr = timings['Fajr']
        sunrise = timings['Sunrise']
        dhuhr = timings['Dhuhr']
        asr = timings['Asr']
        maghrib = timings['Maghrib']
        isha = timings['Isha']
        imsak = timings['Imsak']
        midnight = timings['Midnight']

        # Construct message from variables
        text = (f'Fajr: *{fajr}*'
                '\n'
                f'Sunrise: *{sunrise}*'
                '\n'
                f'Dhuhr: *{dhuhr}*'
                '\n'
                f'Asr: *{asr}*'
                '\n'
                f'Maghrib: *{maghrib}*'
                '\n'
                f'Isha: *{isha}*'
                '\n'
                f'Midnight: *{midnight}*'
                '\n'
                f'Imsak: *{imsak}*'
                '\n\n'
                '*Note: Midnight is when the time for Isha ends. If you intend to fast, imsak signifies the'
                ' time from which the fast begins.*')

        return text

    def getMaddhab(self, maddhab):
        sayStr = ''

        if maddhab in maddhab_list:
            maddhabDict = { 'shafii': '0',
                            'hanafi': '1', }
            maddhab = maddhabDict[maddhab]

        elif maddhab not in maddhab_list and maddhab is not None:
            sayStr = ('The maddhab must be either Hanafi or Shafii. Example: `.prayertimes London 3 Shafii`'
                      '\nDefaulting to Hanafi.')
            maddhab = '1'

        elif maddhab is None:
            sayStr = ('*No maddhab specified. Defaulting to Hanafi.*')
            maddhab = '1'

        return maddhab, sayStr


# Register as cog
def setup(bot):
    bot.add_cog(PrayerTimes(bot))
