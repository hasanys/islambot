import discord
from discord.ext import commands
import requests

icon = 'http://cdn.mysitemyway.com/icons-watermarks/flat-circle-white-on-green/ocha/ocha_infrastructure-mosque/ocha_i' \
       'nfrastructure-mosque_flat-circle-white-on-green_512x512.png'

method_list = ['1', '2', '3', '4', '5']
school_list = ['Hanafi', 'Shafii']


class PrayerTimes:

    def __init__(self, bot):
        self.bot = bot

    @commands.bot.command(pass_context=True)
    async def prayertimes(self, ctx, location: str, method: str = None, school: str = None):

        # Process method - if method is not valid then send an error message
        if method is not None and method not in method_list:
                await self.bot.say('The method must be a number between 1 and 5.'
                                   '\n1 = University of Islamic Sciences, Karachi'
                                   '\n2 = Islamic Society of North America (ISNA)'
                                   '\n3 = Muslim World League (MWL)'
                                   '\n4 = Umm al-Qura, Makkah'
                                   '\n5 = Egyptian General Authority of Survey')

        # Otherwise, if the method is not specified, default to ISNA
        elif method is None:
            method = '2'

        # Now process the maddhab - if maddhab is valid then convert to integers needed for URL:
        if school in school_list:
            school = {
                'Shafii': '0',
                'Hanafi': '1',
            }[school]

        # If maddhab is not valid then send an error message and default to Hanafi
        elif school not in school_list:
            await self.bot.say('The school must be either Hanafi or Shafii. Example: `-prayertimes London 2 Hanafi`'
                               '\nDefaulting to Hanafi.')
            school = '1'

        # If maddhab is not specified, default to Hanafi
        elif school is None:
            school = '1'

        # Now construct URL
        url = f'http://api.aladhan.com/timingsByAddress?address={location}&method={method}&school={school}'

        # Open URL and parse JSON
        try:
            r = requests.get(url)

            data = r.json()

            # Assign variables from JSON
            fajr = data['data']['timings']['Fajr']
            sunrise = data['data']['timings']['Sunrise']
            dhuhr = data['data']['timings']['Dhuhr']
            asr = data['data']['timings']['Asr']
            sunset = data['data']['timings']['Sunset']
            maghrib = data['data']['timings']['Maghrib']
            isha = data['data']['timings']['Isha']
            imsak = data['data']['timings']['Imsak']
            midnight = data['data']['timings']['Midnight']

            # Construct message from variables
            text = f'Fajr: *{fajr}*\n' \
                   f'Sunrise: *{sunrise}*\n' \
                   f'Dhuhr: *{dhuhr}*\n' \
                   f'Asr: *{asr}*\n' \
                   f'Sunset: *{sunset}*\n' \
                   f'Maghrib: *{maghrib}*\n' \
                   f'Isha: *{isha}*\n' \
                   f'Imsak: *{imsak}*\n' \
                   f'Midnight: *{midnight}* '

            # Convert method integers into the actual names
            method = {
                '1': 'University of Islamic Sciences, Karachi',
                '2': 'Islamic Society of North America (ISNA)',
                '3': 'Muslim World League (MWL)',
                '4': 'Umm al-Qura, Makkah',
                '5': 'Egyptian General Authority of Survey',
            }[method]

            # Convert back to maddhab names
            school = {
                '0': "Shafi'i",
                '1': 'Hanafi',
            }[school]

            # Construct and send embed
            em = discord.Embed(title=f"{method} - {school}", description=text, colour=0x78c741)
            em.set_author(name=f'Salat Times for {location}', icon_url=icon)
            await self.bot.say(embed=em)

        except:
            await self.bot.say('The location provided was invalid.')


# Register as cog
def setup(bot):
    bot.add_cog(PrayerTimes(bot))
