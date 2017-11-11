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
The above command would quote Surah 1, Verses 1-7 (Surah al-Fatihah) using the translation of Yusuf Ali.

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
**-aquran** functions in the same way as **-quran**, but quotes the verse in Arabic.

For example, to quote the first verse of the Qu'ran:
```
-aquran 1:1
```

## Tafseer

### -atafsir
**-atafsir** allows you to quote the tasfir (commentary) of verses in Arabic. Currently, Tafsir al-Jalalayn and Tafsir al-Muyassar are available. It works in the same manner as **-quran**.

```
-atafsir <surah>:<verse(s)> [tafsir edition]
```

For example:

```
-atafsir 2:255 muyassar
```
The above command would quote the tafsir of Ayatul Kursi from Tafsir al-Muyassar.

#### Valid tafsir editions
* jalalayn = Tafsir al-Jalalayn

* muyassar = Tafsir al-Muyassar

If no tafsir edition is chosen, it will default to Tafsir al-Jalalayn.

### -tafsir
**-tafsir** allows you to quote the English tasfir (commentary) of verses from Tafsir al-Jalalayn. It works in the same manner as **-aquran**.

```
-tafsir <surah>:<verse(s)> 
```

For example:

```
-tafsir 1:1-7
```
The above command would quote the tafsir of Surah al-Fatihah from Tafsir al-Jalalayn. 

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
**-ahadith** is the same as -hadith, but allows you to quote hadith in Arabic. 


## Prayer (Salaah) Times

The bot can also get prayer times for a specific address/location, with optional parameters for the calculation method and maddhab, either Hanafi or Shafi'i (Shafi'i prayer times are the same as Maliki and Hanbali).

```
-prayertimes <"address/location name"> [method number] [maddhab]
```

For example:
```
-prayertimes "East London Mosque, London" 2 Shafii
```

..would fetch prayer times in the general area of East London Mosque, using the calculation method of ISNA and the Shafi'i maddhab.

#### Valid method integers

* 1 - University of Islamic Sciences, Karachi
* 2 - Islamic Society of North America (ISNA)
* 3 - Muslim World League (MWL)
* 4 - Umm al-Qura, Makkah
* 5 - Egyptian General Authority of Survey
* 7 - Institute of Geophysics, University of Tehran

## Hijri Calendar

The bot can also (rather inaccurately) convert both ways between the Hijri and Gregorian calendars.

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

## Search

The bot can search for Islamic rulings from from several websites, including islamqa.org, islamqa.info and seekershub.org.

### -islamqa
Search for an Islamic ruling on a topic.

```
-islamqa <"topic name">
```

For example:
```
-islamqa "Combining prayers"
```






