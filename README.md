# islambot
A simple Islamic Discord bot with support for Qu'ran, hadith (from sunnah.com), salaah times and conversions to and from the hijri calendar.

Created by Zaify#6850. Contributors: ala and Caleb

## Qu'ran 

### -quran
**-quran** allows you to quote Qu'ran verses in English, with an optional English translation edition.

```
-quran <surah>:<verse(s)> [translation edition]
```

For example:

```
-quran 1:1-7 yusufali 
```
The above command would quote Surah 1, Verses 1-7 (Surah al-Fatihah) using the translation of Yusuf Ali 

#### Valid translation editions
* sahih = Saheeh International

* ahmedali = Ahmed Ali

* ahmedraza = Ahmed Raza Khan Barelvi

* arberry = Arthur John Arberry (Non-Muslim) 

* asad = Muhammad Asad

* daryabadi = Abdul Majid Daryabadi

* hilali = Hilali-Khan

* pickthall = Muhammad Pickthall

* qaribullah = Qaribullah & Darwish

* sarwar = Muhammad Sarwar (Shia) 

* yusufali = Yusuf Ali 

### -aquran
**-aquran** functions in the same way as **-quran**, but quotes the verse in Arabic. Obviously, there is no option for different editions,
as there is only one Arabic Qu'ran. 

For example, to quote the first verse of the Qu'ran:
```
-aquran 1:1
```

## Hadith 

### -hadith
**-hadith** allows you to quote hadith from sunnah.com in English.

```
-hadith <hadith book name> <chapter number>:<hadith number>
```

For example, to quote the second hadith in Chapter 1 of Sahih Bukhari:
```
-hadith bukhari 1:2
```

#### Valid hadith book names 

* bukhari = Sahih Bukhari
* muslim = Sahih Muslim
* tirmidhi = Jami` at-Tirmidhi
* abudawud = Sunan Abi Dawud
* nasai = Sunan an-Nasa'i
* ibnmajah = Sunan Ibn Majah
* malik = Muwatta Malik
* riyadussaliheen = Riyad as-Salihin
* adab = Al-Adab Al-Mufrad
* bulugh = Bulugh al-Maram
* qudsi = 40 Hadith Qudsi
* nawawi = 40 Hadith Nawawi

40 Hadith Qudsi or Nawawi are both 40 hadith long respectively, and as such do not use a chapter number.

For example:
```
-hadith qudsi 32
```

Not all hadith are indexed correctly on sunnah.com, and not all use the same numbering as in the books - so please keep this in mind.

### -ahadith
**-ahadith** allows you to quote hadith from sunnah.com, but in Arabic. Works in the same way as **-hadith**. 


## Prayer (Salaah) Times

The bot can also get prayer times for a specific address/location, with optional parameters for the calculation method and maddhab (either Hanafi or Shafi'i).

```
-prayertimes <"address/location name"> [method number] [maddhab]
```

For example:
```
-prayertimes "East London Mosque, London" 2 Shafii
```

#### Valid method integers

* 1 - University of Islamic Sciences, Karachi
* 2 - Islamic Society of North America (ISNA)
* 3 - Muslim World League (MWL)
* 4 - Umm al-Qura, Makkah
* 5 - Egyptian General Authority of Survey
* 7 - Institute of Geophysics, University of Tehran

## Hijri Calendar

The bot can also (rather inaccurately) convert both ways between the Hijri and Gregorians calendars.

### -convertdate
Converts a Gregorian date to its corresponding Hijri date.

```
-convertdate DD-MM-YY 
```

For example:
```
-convertdate 31-08-2017
```

### -converthijridate
Converts a Hijri date to its corresponding Gregorian date.

For example, to convert 17 Muharram 1407:
```
-converthijridate 17-01-1407
```




