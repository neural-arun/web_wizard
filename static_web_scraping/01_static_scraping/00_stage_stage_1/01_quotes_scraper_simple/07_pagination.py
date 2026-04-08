import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

URL = "https://quotes.toscrape.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}       # ye identity hai

current_url = URL

all_quotes = []

while True:
    response = requests.get(current_url ,headers=HEADERS,timeout=100) # yha request(python browser ka use karke main response ko
# terminal mein la raha hoon)

    soup = BeautifulSoup(response.text,"lxml")       # ye us response ko HTML tree mein badal deta hai.

    quotes = soup.find_all("div", class_="quote")   # yha hm record ko pakad rhe hain


    for quote in quotes:
        text = quote.find("span",class_="text").get_text()  # quotes ke text ko liya
        author = quote.find("small",class_ = "author").get_text()   # Author ko liya
        tags = quote.find_all("a",class_ = "tag")  # tag ki list uthayi
        tag_texts = [tag.get_text() for tag in tags]  #ek ek tag nikal ke append kar diya

        quote_data = {
            "Text" : text,
            "Author" : author,
            "Tags" : tag_texts
        }
        
        all_quotes.append(quote_data)

    next_button = soup.find("li", class_="next")

    if next_button is None:
        break

    next_link = next_button.find("a")["href"]
    current_url = URL + next_link

    import time
    time.sleep(3)



with open(BASE_DIR/"quotes.json",'w',encoding="utf-8") as f:
    json.dump(all_quotes,f,ensure_ascii = False,indent=4)

print("Total quotes scraped:", len(all_quotes))
print("All quotes saved to 'quotes.json'.")