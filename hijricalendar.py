from aiohttp import ClientSession
from discord.ext import commands


class HijriCalendar:

    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession(loop = bot.loop)
        self.toGregorian_url = 'https://api.aladhan.com/hToG?date={date}'
        self.toHijri_url = 'https://api.aladhan.com/gToH?date={date}'

    # Convert from Hijri to Gregorian calendar
    @commands.bot.command(pass_context=True)
    async def converthijridate(self, ctx, date: str):
        """
        Converts a Hijri calendar date to the Gregorian calendar
        """

        # Debug info
        sender = ctx.message.author
        server = ctx.message.server
        serverid = ctx.message.server.id

        print(f'{sender} executed command converthijridate on {server} ({serverid})')

        # Check if the date is in a DD-MM-YY format
        if not self.isInCorrectFormat(date):
            await self.bot.say('Invalid arguments! Do `-converthijridate DD-MM-YY`.\n\n'
                               'Example: `-converthijridate 17-01-1407`(for 17 Muharram 1407)')
            return

        try:
            day, month, year = await self.getConvertedDate(date, getHijri = False)
            await self.bot.say(f'The hijri date {date} is **{day} {month} {year} CE.**')
        except:
            await self.bot.say('An error occurred when trying to convert the date.')

    @commands.bot.command(pass_context=True)
    async def convertdate(self, ctx, date: str):

        """
        Converts a Gregorian calendar date to a Hijri calendar date
        """

        # Debug info
        sender = ctx.message.author
        server = ctx.message.server
        serverid = ctx.message.server.id
        print(f'{sender} executed command convertdate on {server} ({serverid})')

        # Check if the date is in a DD-MM-YY format
        if not self.isInCorrectFormat(date):
            await self.bot.say(
                'Invalid arguments! Do `-convertdate DD-MM-YY`.\n\n'
                'Example: `-convertdate 17-01-2001`')
            return

        try:
            day, month, year = await self.getConvertedDate(date)
            await self.bot.say(f'The date {date} is **{day} {month} {year} AH.**')
        except:
            await self.bot.say('An error occurred when trying to convert the date.')

    async def getConvertedDate(self, date, getHijri = True):
        if getHijri:
            url = self.toHijri_url
        else:
            url = self.toGregorian_url

        async with self.session.get(url.format(date)) as r:
            data = await r.json()

        if getHijri:
            calendar = data['data']['hijri']
        else:
            calendar = data['data']['gregorian']

        day = calendar['month']['number']
        month = calendar['month']['en']
        year = calendar['year']

        return day, month, year

    @staticmethod
    def isInCorrectFormat(date):
        try:
            date.split('-')
            return True
        except:
            return False


# Register as cog
def setup(bot):
    bot.add_cog(HijriCalendar(bot))
