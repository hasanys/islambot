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

    await bot.change_presence(game=discord.Game(name='sunnah.com'))


hadith_book_list = ['bukhari', 'muslim', 'tirmidhi', 'abudawud', 'nasai', 'ibnmajah', 'malik', 'riyadussaliheen', 'adab',
                    'bulugh', 'qudsi', 'nawawi']
icon = 'https://sunnah.com/images/hadith_icon2_huge.png'


@bot.command(pass_context=True)

async def hadith(ctx, book_name : str = None, book_number : int = None, hadith_number: int = None):

    # Initialize and change some variables
    narrator = None
    grading = None
    text = None

    # Construct URL
    if book_name in hadith_book_list:

        # convert qudsi and nawawi to version needed for url (they are special)
        if book_name == 'qudsi':
            book_name = 'qudsi40'

        if book_name == 'nawawi':
            book_name = 'nawawi40'

        if hadith_number is not None:
            url = 'https://sunnah.com/{0}/{1}/{2}'.format(book_name, book_number, hadith_number)

        #40 hadith qudsi and nawawi only accept two arguments
        else:
            url = 'https://sunnah.com/{0}/{1}'.format(book_name,book_number)

    else:
        await bot.send_message(ctx.message.channel, content = "Invalid syntax! Please use -hadith (book name) 
                               (chapter number) (hadith number). Valid book names are `{0}`"
                               .format(hadith_book_list))


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
    if book_name == 'bukhari':
        book_name = 'Sahih Bukhari'

    elif book_name == 'muslim':
        book_name = 'Sahih Muslim'

    elif book_name == 'tirmidhi':
        book_name = 'Jami` at-Tirmidhi'

    elif book_name == 'abudawud':
        book_name = 'Sunan Abi Dawud'

    elif book_name == 'nasai':
        book_name = "Sunan an-Nasa'i"

    elif book_name == 'ibnmajah':
        book_name = 'Sunan Ibn Majah'

    elif book_name == 'malik':
        book_name = 'Muwatta Malik'

    elif book_name == 'riyadussaliheen':
        book_name = 'Riyad as-Salihin'

    elif book_name == 'adab':
        book_name = "Al-Adab Al-Mufrad"

    elif book_name == 'bulugh':
        book_name = 'Bulugh al-Maram'

    elif book_name == 'qudsi40':
        book_name = '40 Hadith Qudsi'

    elif book_name == 'nawawi40':
        book_name = '40 Hadith Nawawi'

    # Construct message

    if text is not None:

        # If hadith has no grading, there is no need to add one
        if grading is None:

            em = discord.Embed(title=narrator, description=hadith_text, colour=0x78c741)

        # Otherwise, if there's a grading, add it
        else:

            em = discord.Embed(title=narrator, description=hadith_text + '\n \n**Grading**: *{0}*'.format(grading), colour=0x78c741)

        # Nawawi and Qudsi are special
        if book_name == 'nawawi40' or 'qudsi40':

            em.set_author(name='{0}, Hadith {1}'.format(book_name, book_number), icon_url=icon)

        # Format for normal hadith
        else:
            em.set_author(name='{0}, Book {1}, Hadith {2}'.format(book_name, book_number, hadith_number), icon_url=icon)

        await bot.send_message(ctx.message.channel, embed=em)

    else:
        await bot.send_message(ctx.message.channel, content='The hadith could not be found on sunnah.com.')



# Arabic hadith


@bot.command(pass_context=True)
async def ahadith(ctx, book_name : str = None, book_number : int = None, hadith_number: int = None):

    grading = None
    text = None
    chapter_name = None

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
        await bot.send_message(ctx.message.channel, content = "Invalid syntax! Please use -hadith (book name) 
                               (chapter number) (hadith number). Valid book names are `{0}`"


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
    if book_name == 'bukhari':
        book_name = 'صحيح البخاري'

    elif book_name == 'muslim':
        book_name = 'صحيح مسلم'

    elif book_name == 'tirmidhi':
        book_name = 'جامع الترمذي'

    elif book_name == 'abudawud':
        book_name = 'سنن أبي داود'

    elif book_name == 'nasai':
        book_name = "سنن النسائي"

    elif book_name == 'ibnmajah':
        book_name = 'سنن ابن ماجه'

    elif book_name == 'malik':
        book_name = 'موطأ مالك'

    elif book_name == 'riyadussaliheen':
        book_name = 'رياض الصالحين'

    elif book_name == 'adab':
        book_name = "الأدب المفرد"

    elif book_name == 'bulugh':
        book_name = 'بلوغ المرام'

    elif book_name == 'qudsi40':
        book_name = 'الأربعون القدسية'

    elif book_name == 'nawawi40':
        book_name = 'الأربعون النووية'


    # Construct message

    if text is not None:
        em = discord.Embed(title=chapter_name, description=hadith_text, colour=0x78c741)

        if book_name == 'nawawi40' or 'qudsi40':
            em.set_author(name='{0} حديث, {1}'.format(book_number, book_name), icon_url=icon)

        else:

            em.set_author(name='{0} حديث , {1} كتاب , {2}'.format(hadith_number, book_number, book_name), icon_url=icon)

        await bot.send_message(ctx.message.channel, embed=em)

    else:

        await bot.send_message(ctx.message.channel, content='The hadith could not be found on sunnah.com.')



bot.run('token')
