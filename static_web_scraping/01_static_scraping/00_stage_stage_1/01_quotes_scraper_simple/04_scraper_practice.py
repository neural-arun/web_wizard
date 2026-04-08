import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}       # ye identity hai

response = requests.get(URL,headers=HEADERS) # yha request(python browser ka use karke main response ko
# terminal mein la raha hoon)

soup = BeautifulSoup(response.text,"lxml")       # ye us response ko HTML tree mein badal deta hai.

quotes = soup.find_all("div", class_="quote")   # yha hm record ko pakad rhe hain

for quote in quotes:
    text = quote.find("span",class_="text").get_text()  # quotes ke text ko liya
    author = quote.find("small",class_ = "author").get_text()   # Author ko liya
    tags = quote.find_all("a",class_ = "tag")  # tag ki list uthayi
    tag_texts = [tag.get_text() for tag in tags]  #ek ek tag nikal ke append kar diya

    print(f"Quote: {text}")
    print(f"Author: {author}")
    print(f"Tags: {tag_texts}")
    print("#"* 50)
