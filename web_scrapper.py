#########################################################
# This section is used to create the web scrapper       #
# to obtain the different versions of the bible to      #
# be analyzed.                                          #
#########################################################

import pandas as pd
import numpy as np
import bs4
import requests
import random
from random import randint
import time
import re
from helper_lists import user_agents

def bible_scraper(web_number: int, version: str) -> None:
    """
    A web scraping function to extract the contents of The Bible from the website `bible.com`.
    :param web_number: The Bible version numerical code in the URL from the website
    :param version: The actual version of the Bible (e.g. NIV / KJV)
    :return: None (the function save each book as a .csv file in the specified drive)
    """

    books = ['GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', '1SA', '2SA', '1KI',
             '2KI', '1CH', '2CH', 'EZR', 'NEH', 'EST', 'JOB', 'PSA', 'PRO', 'ECC', 'SNG',
             'ISA', 'JER', 'LAM', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO', 'OBA', 'JON', 'MIC',
             'NAM', 'HAB', 'ZEP', 'HAG', 'ZEC', 'MAL', 'MAT', 'MRK', 'LUK', 'JHN', 'ACT',
             'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI',
             'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV']
    base_url = "https://www.bible.com/bible/"
    headers = {"User-Agent": random.choice(user_agents)}

    for book in books:
        book_data = []

        for chapter in range(1, 151):
            url = f"{base_url}{web_number}/{book}.{chapter}.{version}"
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = bs4.BeautifulSoup(response.content, "lxml")
                    for verse in range(1, 177):
                        verse_selector = f"{book}.{chapter}.{verse}"
                        verse_elements = soup.find_all("span", attrs={"data-usfm": verse_selector})

                        if verse_elements:
                            full_text = []
                            for element in verse_elements:
                                content_spans = element.find_all("span", class_=["ChapterContent_content__RrUqA", "ChapterContent_add__9EgW2", "ChapterContent_nd__ECPAf"])
                                full_text.append(''.join(span.get_text() for span in content_spans))

                            book_data.append({
                                'Book': book,
                                'Chapter': chapter,
                                'Verse': verse,
                                'Text': ' '.join(full_text).strip()
                            })

            except requests.RequestException as e:
                print(f"Error scraping {url}: {e}")

        df = pd.DataFrame(book_data)
        df.to_csv(f'./Texts/{version}/{book.lower()}.csv', index=False)


# KJV: https://www.bible.com/bible/1/GEN.1.KJV
# NKJV: https://www.bible.com/bible/114/GEN.1.NKJV
# NIV: https://www.bible.com/bible/111/GEN.1.NIV
# NRSV: https://www.bible.com/bible/2016/GEN.1.NRSV
# ESV: https://www.bible.com/bible/59/GEN.1.ESV

bible_scraper(59, "ESV")