from discord.ext import commands
import requests


class HijriCalendar:

    def __init__(self, bot):
        self.bot = bot

    # Convert from Hijri to Gregorian calendar
    @commands.bot.command(pass_context=True)
    async def converthijridate(self, ctx, date: str):

        '''
        Converts a Hijri calendar date to the Gregorian calendar
        '''

        # Debug info
        sender = ctx.message.author
        server = ctx.message.server
        serverid = ctx.message.server.id
        print(f'{sender} executed command converthijridate on {server} ({serverid})')

        # Check if the date is in a DD-MM-YY format
        try:
            day, month, year = date.split('-')

        except:
            await self.bot.say('Invalid arguments! Do `-converthijridate DD-MM-YY`.\n\nExample: `-converthijridate 7-01'
                               '-1407`(for 17 Muharram 1407)')
            return

        # Construct URL
        url = f'https://api.aladhan.com/hToG?date={date}'

        try:
            # Open URL and parse JSON
            r = requests.get(url)

            data = r.json()

            # Assign variables from JSON
            day = data['data']['gregorian']['month']['number']
            month = data['data']['gregorian']['month']['en']
            year = data['data']['gregorian']['year']

            # Construct message from variables
            await self.bot.say(f'The hijri date {date} is **{day} {month} {year} CE.**')

        # If the date isn't on the API, send an error message
        except:
            await self.bot.say('An error occurred when trying to convert the date.')

        # Convert from Gregorian to Hijri calendar

    @commands.bot.command(pass_context=True)
    async def convertdate(self, ctx, date: str):

        '''
        Converts a Gregorian calendar date to a Hijri calendar date
        '''

        # Debug info
        sender = ctx.message.author
        server = ctx.message.server
        serverid = ctx.message.server.id
        print(f'{sender} executed command convertdate on {server} ({serverid})')

        # Check if the date is in a DD-MM-YY format
        try:
            day, month, year = date.split('-')

        except:
            await self.bot.say(
                'Invalid arguments! Do `-convertdate DD-MM-YY`.\n\nExample: `-convertdate 17-01-2001`')
            return

        # Construct URL
        url = f'https://api.aladhan.com/gToH?date={date}'

        try:
            # Open URL and parse JSON
            r = requests.get(url)

            data = r.json()

            # Assign variables from JSON
            day = data['data']['hijri']['month']['number']
            month = data['data']['hijri']['month']['en']
            year = data['data']['hijri']['year']

            # Construct message from variables
            await self.bot.say(f'The date {date} is **{day} {month} {year} AH.**')

        # If the date isn't on the API, send an error message
        except:
            await self.bot.say('An error occurred when trying to convert the date.')


# Register as cog
def setup(bot):
    bot.add_cog(HijriCalendar(bot))
