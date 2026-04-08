import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(URL, headers=HEADERS)
print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "lxml")     #  HTML ko tree bana diya.
print("Soup type:", type(soup))

quotes = soup.find_all("div", class_="quote")     # is tarah ke saare cheezo ko pakdo.
print("Total quotes found:", len(quotes))

first_quote = quotes[0]
print(first_quote)
