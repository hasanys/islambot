import discord
from discord.ext import commands
import requests

icon = 'http://cdn.mysitemyway.com/icons-watermarks/flat-circle-white-on-green/ocha/ocha_infrastructure-mosque/ocha_i' \
       'nfrastructure-mosque_flat-circle-white-on-green_512x512.png'

method_list = ['1', '2', '3', '4', '5']
maddhab_list = ['hanafi', 'shafii']


class PrayerTimes:

    def __init__(self, bot):
        self.bot = bot

    @commands.bot.command(pass_context=True)
    async def prayertimes(self, ctx, location: str, method: str = None, maddhab: str = None):

        # Process method - if method is not valid then send an error message
        if method is not None and method not in method_list:
                await self.bot.say('The method must be a number between 1 and 5.```'
                                   '\n1 = University of Islamic Sciences, Karachi'
                                   '\n2 = Islamic Society of North America (ISNA)'
                                   '\n3 = Muslim World League (MWL)'
                                   '\n4 = Umm al-Qura, Makkah'
                                   '\n5 = Egyptian General Authority of Survey```')
                return

        # Otherwise, if the method is not specified, default to Umm al-Qura
        elif method is None:
            await self.bot.say('*No method specified. Defaulting to Umm al-Qura, Makkah.*')
            method = '4'

        # Allow maddhab to be typed in different cases:
        if maddhab is not None:
            maddhab = maddhab.lower()

        # Now process the maddhab - if maddhab is valid then convert to integers needed for URL:
        if maddhab in maddhab_list:
            maddhab = {
                'shafii': '0',
                'hanafi': '1',
                }[maddhab]

        # If maddhab is not valid then send an error message and default to Hanafi
        elif maddhab not in maddhab_list and maddhab is not None:
            await self.bot.say('The maddhab must be either Hanafi or Shafii. Example: `.prayertimes London 3 Shafii`'
                               '\nDefaulting to Hanafi.')
            maddhab = '1'

        # If maddhab is not specified, default to Hanafi
        elif maddhab is None:
            await self.bot.say('*No maddhab specified. Defaulting to Hanafi.*')
            maddhab = '1'

        # Now construct URL
        url = f'http://api.aladhan.com/timingsByAddress?address={location}&method={method}&school={maddhab}'

        try:
            # Open URL and parse JSON
            r = requests.get(url)

            data = r.json()

            # Assign variables from JSON
            fajr = data['data']['timings']['Fajr']
            sunrise = data['data']['timings']['Sunrise']
            dhuhr = data['data']['timings']['Dhuhr']
            asr = data['data']['timings']['Asr']
            maghrib = data['data']['timings']['Maghrib']
            isha = data['data']['timings']['Isha']
            imsak = data['data']['timings']['Imsak']
            midnight = data['data']['timings']['Midnight']

            # Construct message from variables
            text = f'Fajr: *{fajr}*\n' \
                    f'Sunrise: *{sunrise}*\n' \
                    f'Dhuhr: *{dhuhr}*\n' \
                    f'Asr: *{asr}*\n' \
                    f'Maghrib: *{maghrib}*\n' \
                    f'Isha: *{isha}*\n' \
                    f'Midnight: *{midnight}*\n' \
                    f'Imsak: *{imsak}*\n\n' \
                   '*Note: Midnight is when the time for Isha ends. If you intend to fast, imsak signifies the' \
                   ' time from which the fast begins.*'

            # Convert method integers into the actual names
            method = {
                '1': 'University of Islamic Sciences, Karachi',
                '2': 'Islamic Society of North America (ISNA)',
                '3': 'Muslim World League (MWL)',
                '4': 'Umm al-Qura, Makkah',
                '5': 'Egyptian General Authority of Survey',
            }[method]

            # Convert back to maddhab names
            maddhab = {
                '0': "Shafi'i",
                '1': 'Hanafi',
            }[maddhab]

            # Construct and send embed
            em = discord.Embed(title=f"{method} - {maddhab}", description=text, colour=0x78c741)
            em.set_author(name=f'Salat Times for {location}', icon_url=icon)
            await self.bot.say(embed=em)

        except:
            await self.bot.say('Invalid arguments! Usage: `.prayertimes [location] [method] [maddhab]`.\n'
                               'Example: `.prayertimes London 4 Shafii`\n'
                               'You can include multiple words in the location by enclosing it in quotes. Example:'
                               '`.prayertimes "East London Mosque" 4 Shafii`')


# Register as cog
def setup(bot):
    bot.add_cog(PrayerTimes(bot))
