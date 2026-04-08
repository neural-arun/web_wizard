import requests

URL = "https://quotes.toscrape.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(URL,headers=HEADERS)

print(f"status code : {response.status_code}")

print(response.text[:500])