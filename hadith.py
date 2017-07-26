from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import requests

hadith_book_list = ['bukhari', 'muslim', 'tirmidhi', 'abudawud', 'nasai', 'ibnmajah', 'malik', 'riyadussaliheen', 'adab',
                    'bulugh', 'qudsi', 'nawawi']

icon = 'https://sunnah.com/images/hadith_icon2_huge.png'
error = 'The hadith could not be found on sunnah.com. This could be because it does not exist, ' \
        'or due to the irregular structure of the website.'


class Hadith:

    def __init__(self, bot):
        self.bot = bot

    @commands.bot.command(pass_context=True)
    async def hadith(self, ctx, book_name : str = None, book_number : int = None, hadith_number: int = None):

        # Initialize and change some variables
        narrator = None
        grading = None
        text = None
        url = None

        # Construct URL
        if book_name in hadith_book_list:

            # Convert Qudsi and Nawawi to version needed for URL (they are special)
            if book_name == 'qudsi':
                book_name = 'qudsi40'

            if book_name == 'nawawi':
                book_name = 'nawawi40'

            if hadith_number is not None:
                url = f'https://sunnah.com/{book_name}/{book_number}/{hadith_number}'

            # 40 Hadith Qudsi and Nawawi only accept two arguments
            else:
                url = f'https://sunnah.com/{book_name}/{book_number}'

        else:
            await self.bot.say(f'Invalid arguments! Please do `-hadith (book name) (book number) (hadith number)`'
                          f' \nValid book names are `{hadith_book_list}`')

        # Setup scanner
        r = requests.get(url)
        data = r.text
        scanner = BeautifulSoup(data, "html.parser")

        # Get raw hadith text
        for hadith in scanner.findAll("div", {"class": "text_details"}):
            text = hadith.text
        hadith_text = str(text)

        # Remove " ` " character as it conflicts with Discord markup and remove excess spaces
        hadith_text = hadith_text.replace("`", "")
        hadith_text = hadith_text.replace("     ", "")

        # Get narrator (if applicable)
        for hadith in scanner.findAll("div", {"class": "hadith_narrated"}):
            narrator = hadith.text

        # Get grading (if applicable)
        for hadith in scanner.findAll("td", {"class": "english_grade"}):
            grading = hadith.text

        # Format book name
        book_name = {
            'bukhari': 'Sahih Bukhari',
            'muslim': 'Sahih Muslim',
            'tirmidhi': 'Jami` at-Tirmidhi',
            'abudawud': 'Sunan Abi Dawud',
            'nasai': "Sunan an-Nasa'i",
            'ibnmajah': 'Sunan Ibn Majah',
            'malik': 'Muwatta Malik',
            'riyadussaliheen': 'Riyad as-Salihin',
            'adab': "Al-Adab Al-Mufrad",
            'bulugh': 'Bulugh al-Maram',
            'qudsi40': '40 Hadith Qudsi',
            'nawawi40': '40 Hadith Nawawi'
        }[book_name]

        # Construct message
        if text is not None:

            # If hadith has no grading, don't add it
            if grading is None:
                em = discord.Embed(title=narrator, description=hadith_text, colour=0x78c741)

            # Otherwise, if there's a grading, add it
            else:
                em = discord.Embed(title=narrator, description=hadith_text + '\n \n**Grading**: *{0}*'.format(grading),
                                   colour=0x78c741)

            #  Formatting for normal hadith
            if book_name != '40 Hadith Nawawi' and book_name != '40 Hadith Qudsi':

                em.set_author(name=f'{book_name} {book_number}:{hadith_number}', icon_url=icon)

            # Formatting for Qudsi and Nawawi
            else:
                em.set_author(name=f'{book_name}, Hadith {book_number}', icon_url=icon)

            # Attempt to send message
            try:
                await self.bot.say(embed=em)

            # If the hadith is too long, shorten it
            except Exception:

                # Remake embed if not Nawawi or Qudsi
                if book_name != '40 Hadith Nawawi' and book_name != '40 Hadith Qudsi':
                    em = discord.Embed(title=narrator, description=hadith_text[:1500]+'...'+f'\n \n*Full hadith:* {url}'
                                       ,icon_url=icon, colour=0x78c741)
                    em.set_author(name=f'{book_name} {book_number}:{hadith_number}', icon_url=icon)

                # Remake embed if Nawawi or Qudsi
                else:
                    em = discord.Embed(title=narrator, description=hadith_text[:1500]+'...'+f'\n \n*Full hadith:* {url}'
                                       ,icon_url=icon, colour=0x78c741)
                    em.set_author(name=f'{book_name}, Hadith {book_number}', icon_url=icon)

                await self.bot.say('This hadith was too long to send. Sending first 1500 characters:',embed=em)

        else:

            await self.bot.say(error)


    # Arabic hadith
    @commands.command(pass_context=True)
    async def ahadith(self, ctx, book_name : str = None, book_number : int = None, hadith_number: int = None):

        text = None
        chapter_name = None
        url = None

        # Construct URL
        if book_name in hadith_book_list:

            # convert qudsi and nawawi to version needed for url (they are special)
            if book_name == 'qudsi':
                book_name = 'qudsi40'

            if book_name == 'nawawi':
                book_name = 'nawawi40'

            if hadith_number is not None:
                url = f'https://sunnah.com/{book_name}/{book_number}/{hadith_number}'

            else:
                url = f'https://sunnah.com/{book_name}/{book_number}'

        else:

            await self.bot.say(f'Invalid arguments! Please do `-ahadith (book name) (book number) (hadith number)`'
                               f' \nValid book names are `{hadith_book_list}`')

        # Setup scanner
        r = requests.get(url)
        data = r.text
        scanner = BeautifulSoup(data, "html.parser")

        # Get raw hadith text
        for hadith in scanner.findAll("div", {"class": "arabic_hadith_full arabic"}):
            text = hadith.text
        hadith_text = str(text)

        # Get chapter name
        for hadith in scanner.findAll("div", {"class": "arabicchapter arabic"}):
            chapter_name = hadith.text

        # Translate book name into Arabic
        book_name = {
            'bukhari': 'صحيح البخاري',
            'muslim': 'صحيح مسلم',
            'tirmidhi': 'جامع الترمذي',
            'abudawud': 'سنن أبي داود',
            'nasai': "سنن النسائي",
            'ibnmajah': 'سنن ابن ماجه',
            'malik': 'موطأ مالك',
            'riyadussaliheen': 'رياض الصالحين',
            'adab': "الأدب المفرد",
            'bulugh': 'بلوغ المرام',
            'qudsi40': 'الأربعون القدسية',
            'nawawi40': 'الأربعون النووية'
        }[book_name]

        # Construct message
        if text is not None:
            em = discord.Embed(title=chapter_name, description=hadith_text, colour=0x78c741)

            # Formatting for normal hadith
            if book_name != 'الأربعون النووية' and book_name != 'الأربعون القدسية':
                em.set_author(name=f'({book_number}:{hadith_number}) - {book_name}', icon_url=icon)

            # Formatting for Qudsi and Nawawi (Arabic has to be in weird place for it to show on Discord properly)
            else:
                em.set_author(name=f'{book_number} {book_name} , حديث', icon_url=icon)

            # Attempt to send message
            try:
                await self.bot.say(embed=em)

            # If the hadith is too long, shorten it
            except Exception:

                # Remake embed if not Qudsi or Nawawi
                if book_name != 'الأربعون النووية' and book_name != 'الأربعون القدسية':
                    em = discord.Embed(title=chapter_name, description=hadith_text[:1500]+'...'+f'\n \n*Full hadith:*'
                                       f' {url}', colour=0x78c741)
                    em.set_author(name=f'({book_number}:{hadith_number}) - {book_name}', icon_url=icon)

                # Remake embed if Qudsi or Nawawi
                else:
                    em = discord.Embed(title="", description=hadith_text[:1500]+'...'+f'\n \n*Full hadith:*'
                                       f' {url}', colour=0x78c741)
                    em.set_author(name=f'{book_number} {book_name} , حديث', icon_url=icon)

                await self.bot.say('This hadith was too long to send. Sending first 1500 characters:',embed=em)

        else:
            await self.bot.say(error)


# Register as cog
def setup(bot):
    bot.add_cog(Hadith(bot))
