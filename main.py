#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import requests

description = '''A Discord bot which allows you to search ahadith from
sunnah.com.'''

bot = commands.Bot(command_prefix='-', description=description)


# Setup
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

    await bot.change_presence(game=discord.Game(name='-hadith to search ahadith'))


hadith_book_list = ['bukhari', 'muslim', 'tirmidhi', 'abudawud', 'nasai', 'ibnmajah', 'malik', 'riyadussaliheen', 'adab',
                    'bulugh', 'qudsi', 'nawawi']

icon = 'https://sunnah.com/images/hadith_icon2_huge.png'
error = 'The hadith could not be found on sunnah.com. This could be because it does not exist under that numbering, ' \
        'or due to the irregular structure of the website.'


@bot.command(pass_context=True)
async def hadith(ctx, book_name : str = None, book_number : int = None, hadith_number: int = None):

    # Initialize and change some variables
    narrator = None
    grading = None
    text = None
    url = None

    # Construct URL
    if book_name in hadith_book_list:

        # convert qudsi and nawawi to version needed for url (they are special)
        if book_name == 'qudsi':
            book_name = 'qudsi40'

        if book_name == 'nawawi':
            book_name = 'nawawi40'

        if hadith_number is not None:
            url = 'https://sunnah.com/{0}/{1}/{2}'.format(book_name, book_number, hadith_number)

        # 40 hadith qudsi and nawawi only accept two arguments
        else:
            url = 'https://sunnah.com/{0}/{1}'.format(book_name,book_number)

    else:
        await bot.say('Invalid arguments! Please do `-hadith (book name) (book number) (hadith number)`'
                      ' \n Valid book names are `{0}`'.format(hadith_book_list))


    # Setup scanner
    r = requests.get(url)
    data = r.text
    scanner = BeautifulSoup(data, "html.parser")


    # Get raw hadith text
    for hadith in scanner.findAll("div", {"class": "text_details"}):
        text = hadith.text
    hadith_unformatted = str(text)


    # Remove '`' characters, as they are used by Discord for formatting
    hadith_semiformatted = hadith_unformatted.replace("`", "")


    # Remove excess spaces
    hadith_text = hadith_semiformatted.replace("     ", "")


    # Get narrator (if applicable)
    for hadith in scanner.findAll("div", {"class": "hadith_narrated"}):
        narrator = hadith.text


    # Get grading
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
        if book_name is not '40 Hadith Nawawi' or '40 Hadith Qudsi':

            em.set_author(name='{0}, Book {1}, Hadith {2}'.format(book_name, book_number, hadith_number), icon_url=icon)

        # Formatting for Qudsi and Nawawi
        else:

            em.set_author(name='{0}, Hadith {1}'.format(book_name, book_number), icon_url=icon)

        await bot.send_message(ctx.message.channel, embed=em)

    else:

        await bot.say(error)



# Arabic hadith


@bot.command(pass_context=True)
async def ahadith(ctx, book_name : str = None, book_number : int = None, hadith_number: int = None):

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
            url = 'https://sunnah.com/{0}/{1}/{2}'.format(book_name, book_number, hadith_number)

        else:
            url = 'https://sunnah.com/{0}/{1}'.format(book_name, book_number)

    else:

        await bot.say('Invalid arguments! Please do `-hadith (book name) (book number) (hadith number)`'
                      ' \n Valid book names are `{0}`'.format(hadith_book_list))


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
        if book_name is not  'الأربعون النووية' or 'الأربعون القدسية':

            em.set_author(name='{2} - كتاب {1} - حديث {0}'.format(hadith_number, book_number, book_name), icon_url=icon)

        # Formatting for Qudsi and Nawawi
        else:
            em.set_author(name='{1} - حديث {0}' .format(book_number, book_name), icon_url=icon)

        await bot.send_message(ctx.message.channel, embed=em)

    else:

        await bot.say(error)



bot.run(token)