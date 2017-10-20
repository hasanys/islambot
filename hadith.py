import re
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from aiohttp import ClientSession

hadith_book_list = ['bukhari', 'muslim', 'tirmidhi', 'abudawud', 'nasai', 'ibnmajah', 'malik', 'riyadussaliheen',
                    'adab', 'bulugh', 'qudsi', 'nawawi']

icon = 'https://sunnah.com/images/hadith_icon2_huge.png'
error = ('The hadith could not be found on sunnah.com. This could be because it does not exist, '
         'or due to the irregular structure of the website.')


class HadithGrading:
    def __init__(self):
        self.narrator = None
        self.grading = None

        self.book_number = None
        self.hadith_number = None

        self.hadithText = None
        self.chapter_name = None


class HadithSpecifics:
    def __init__(self, book_name, session):
        self.session = session

        self.raw_text = None
        self.url = 'https://sunnah.com/{}/{}'

        self.book_name = book_name
        self.readableBookName = None

        self.hadith = HadithGrading()

    def processRef(self, ref):
        if self.book_name not in ['qudsi', 'nawawi']:
            self.hadith.book_number, self.hadith.hadith_number = ref.split(":")
            self.url = self.url.format(self.book_name, self.hadith.hadith_number) + f'/{self.hadith.hadith_number}'

        else:
            self.hadith.hadith_number = ref
            self.book_name = self.book_name + '40'
            self.url = self.url.format(self.book_name, self.hadith.hadith_number)

    async def getHadith(self):
        async with self.session.get(self.url) as resp:
            data = await resp.read()
        scanner = BeautifulSoup(data, "html.parser")

        for hadith in scanner.findAll("div", {"class": "text_details"}):
            self.raw_text = hadith.text

        self.hadith.hadithText = self.formatHadithText(self.raw_text)

        for hadith in scanner.findAll("div", {"class": "hadith_narrated"}):
            self.hadith.narrator = hadith.text

        for hadith in scanner.findAll("td", {"class": "english_grade"}):
            self.hadith.grading = hadith.text

        self.readableBookName = self.formatEnglishBookName(self.book_name)

    async def getArabicHadith(self):
        async with self.session.get(self.url) as resp:
            data = await resp.read()
        scanner = BeautifulSoup(data, "html.parser")

        # Get raw hadith text
        for hadith in scanner.findAll("div", {"class": "arabic_hadith_full arabic"}):
            self.raw_text = hadith.text
        self.hadith.hadithText = str(self.raw_text)

        # Get chapter name
        for hadith in scanner.findAll("div", {"class": "arabicchapter arabic"}):
            self.hadith.chapter_name = hadith.text

        self.readableBookName = self.formatArabicBookName(self.book_name)

    def makeEmbed(self):
        messageText = None
        if len(self.hadith.hadithText) < 1900:
            description = self.hadith.hadithText
        else:
            description = self.hadith.hadithText[:1900] + '...' + f'\n \n*Full hadith:* {self.url}'
            messageText = 'This hadith was too long to send. Sending first 1900 characters:'
        if self.hadith.grading:
            description += f'\n \n**Grading**{self.hadith.grading}'

        if self.book_name not in ['qudsi40', 'nawawi40']:
            authorName = f'{self.readableBookName} {self.hadith.book_number}:{self.hadith.hadith_number}'
        else:
            authorName = f'{self.readableBookName}, Hadith {self.hadith.hadith_number}'

        em = discord.Embed(title = self.hadith.narrator, description = description, colour = 0x78c741)
        em.set_author(name = authorName, icon_url = icon)

        return em, messageText

    def makeEmbedArabic(self):
        messageText = None
        if len(self.hadith.hadithText) < 1900:
            description = self.hadith.hadithText
        else:
            description = self.hadith.hadithText[:1900] + '...' + f'\n \n*Full hadith:* {self.url}'
            messageText = 'This hadith was too long to send. Sending first 1900 characters:'

        if self.book_name not in ['qudsi40', 'nawawi40']:
            authorName = f'({self.hadith.book_number}:{self.hadith.hadith_number}) - {self.readableBookName}'
        else:
            authorName = f'{self.hadith.hadith_number} {self.readableBookName} , حديث'

        em = discord.Embed(title = self.hadith.chapter_name, description = description, colour = 0x78c741)
        em.set_author(name = authorName, icon_url = icon)

        return em, messageText

    @staticmethod
    def formatHadithText(text):
        txt = str(text) \
            .replace('`', '\\`') \
            .replace('\n', '') \
            .replace('<i>', '*') \
            .replace('</i>', '*')

        return re.sub('\s+', ' ', txt)

    @staticmethod
    def formatEnglishBookName(book_name):
        bookDict = {
            'bukhari'        : 'Sahih Bukhari',
            'muslim'         : 'Sahih Muslim',
            'tirmidhi'       : 'Jami` at-Tirmidhi',
            'abudawud'       : 'Sunan Abi Dawud',
            'nasai'          : "Sunan an-Nasa'i",
            'ibnmajah'       : 'Sunan Ibn Majah',
            'malik'          : 'Muwatta Malik',
            'riyadussaliheen': 'Riyad as-Salihin',
            'adab'           : "Al-Adab Al-Mufrad",
            'bulugh'         : 'Bulugh al-Maram',
            'qudsi40'        : '40 Hadith Qudsi',
            'nawawi40'       : '40 Hadith Nawawi'
        }

        return bookDict[book_name]

    @staticmethod
    def formatArabicBookName(book_name):
        bookDict = {
            'bukhari'        : 'صحيح البخاري',
            'muslim'         : 'صحيح مسلم',
            'tirmidhi'       : 'جامع الترمذي',
            'abudawud'       : 'سنن أبي داود',
            'nasai'          : "سنن النسائي",
            'ibnmajah'       : 'سنن ابن ماجه',
            'malik'          : 'موطأ مالك',
            'riyadussaliheen': 'رياض الصالحين',
            'adab'           : "الأدب المفرد",
            'bulugh'         : 'بلوغ المرام',
            'qudsi40'        : 'الأربعون القدسية',
            'nawawi40'       : 'الأربعون النووية'
        }

        return bookDict[book_name]


class Hadith:
    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession(loop = bot.loop)

    @commands.bot.command()
    async def hadith(self, book_name: str = None, ref: str = None):

        if book_name in hadith_book_list:
            spec = self.getSpec(book_name, ref, self.session)
        else:
            await self.bot.say(f'Invalid arguments! Please do `.hadith (book name) (book number) (hadith number)` \n'
                               f'Valid book names are `{hadith_book_list}`')
            return
        await spec.getHadith()

        if spec.hadith.hadithText is not None:
            em, messageText = spec.makeEmbed()
            await self.bot.say(messageText, embed=em)
        else:
            await self.bot.say(error)

    @commands.command()
    async def ahadith(self, book_name: str, ref: str = None):

        if book_name in hadith_book_list:
            spec = self.getSpec(book_name, ref, self.bot)
        else:
            await self.bot.say(f'Invalid arguments! Please do `.hadith (book name) (book number) (hadith number)` \n'
                               f'Valid book names are `{hadith_book_list}`')
            return

        await spec.getArabicHadith()

        if spec.hadith.hadithText is not None:
            em, messagetxt = spec.makeEmbedArabic()
            await self.bot.say(messagetxt, embed=em)
        else:
            await self.bot.say(error)

    @staticmethod
    def getSpec(book_name, ref, session):
        spec = HadithSpecifics(book_name, session)
        spec.processRef(ref)
        return spec


# Register as cog
def setup(bot):
    bot.add_cog(Hadith(bot))
