import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "lxml")

quotes = soup.find_all("div", class_="quote")

for quote in quotes:
    text = quote.find("span", class_="text").get_text()
    author = quote.find("small", class_="author").get_text()
    tags = quote.find_all("a", class_="tag")
    tag_texts = [tag.get_text() for tag in tags]

    print("TEXT:", text)
    print("AUTHOR:", author)
    print("TAGS:", tag_texts)
    print("-" * 50)
