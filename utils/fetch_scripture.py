import requests
from bs4 import BeautifulSoup
import re

def get_verse(passage="John 3:16", version="KJV"):
    url = f"https://www.biblegateway.com/passage/?search={passage}&version={version}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", class_="passage-text")

        if content_div:
            # Remove all footnote <sup> and cross-reference <a> tags
            for tag in content_div.find_all(["sup", "a"]):
                tag.decompose()
            # Remove headings and verse numbers
            for heading in content_div.find_all(class_=["passage-display", "passage-copyright", "passage-reference", "chapternum", "versenum"]):
                heading.decompose()
            # Get only the verse text
            verses = content_div.get_text(separator=" ", strip=True)
            # Clean up extra spaces
            verses = re.sub(r'\s+', ' ', verses).strip()
            return verses
        else:
            return "Could not extract verse content."
    else:
        return "Failed to retrieve passage."

import requests
from bs4 import BeautifulSoup

def get_bible_verse(reference):
    url = f"https://www.biblegateway.com/passage/?search={reference}&version=APSD-CEB"
    headers = {"User-Agent": "Mozilla/5.0"}  # mimic a browser request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        verses = soup.find_all("div", class_="passage-text")

        for verse in verses:
            text = verse.get_text(separator="\n", strip=True)
            print(text)
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

# Example use
get_bible_verse("Panultihon 16:25")
