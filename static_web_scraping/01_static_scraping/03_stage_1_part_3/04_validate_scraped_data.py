import time
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from urllib.parse import urljoin


class BooksScraper:
    def __init__(self,base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.book_data = []

    def fetch_html(self, url):
        try:

            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                response.encoding = "utf-8"
                return response.text
            elif response.status_code == 404:
                print(f"[404] Page not found {url}")
                return None
            elif response.status_code == 403:
                print(f"[403] blocked by server")
                return None
            elif response.status_code == 429:
                print(f"[429] Too many requests")
                return None
            else:
                print(f"{response.status_code} unexpected response. {url}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"[Network error]: {e}")
            return None

    
    def parse_html(self,html):
        return BeautifulSoup(html,"lxml")
    
    def is_valid_book(self,book):
        """
        here we have created a function which checks the book and returns if book is valid or not.
        """
        if not book.get("Price"):
            return False
        if not book.get("Title"):
            return False
        if not book.get("availability"):
            return False
        return True
    

    def extract_records(self,soup):
        
        records = soup.find_all("article",class_="product_pod")
        for record in records:
            title = record.find("h3").find("a")["title"]
            # RATINGS = {"One", "Two", "Three", "Four", "Five"}
            rating = None
            rating_tag = record.find("p")
            if rating_tag and rating_tag.has_attr("class"):
                for cls in rating_tag["class"]:
                    if cls in {"One", "Two", "Three", "Four", "Five"}:
                        rating = cls
                        break
            # If you access rating_tag["class"], you get the list of class names:["star-rating", "Three"].
            price = None
            for p in record.find_all("p"):
                if p.text and "£" in p.text:
                    price = p.text.strip()
                    break
            availability = None
            for a in record.find_all("p"):
                text = a.text.strip().lower()
                if "stock" in text:
                    availability = a.text.strip()
                    break

            

            one_book_data = {
                "Title": title,
                "Rating": rating,
                "Price": price,
                "Availability": availability
            }

            if not self.is_valid_book(one_book_data):
                continue
            # here we are checking if the book is valid or not ?? if valid append if not valid skip.
            self.book_data.append(one_book_data)
    
    def extract_all_pages(self):
        current_url = self.base_url
        while True:
            html = self.fetch_html(current_url)
            if html is None:
                # Page failed skip safely.
                print(f"[Skipping page]: {current_url}")
                break   # break laga rahe kyonki pagination ka next link soup se aata hai aur 
                        # soup hai hi nahi kyonki page hi nahi aaya.

            soup = self.parse_html(html)
            self.extract_records(soup)
            time.sleep(2)
            next_button = soup.find("li",class_="next")
            if not next_button:
                break
            next_link = next_button.find("a")["href"]
            current_url = urljoin(current_url, next_link)


    def save_to_json(self,filename="books_data.json"):
        BASE_DIR = Path(__file__).parent
        file = BASE_DIR/ filename
        with open(file, "w", encoding="utf-8") as f:
            json.dump(self.book_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    books_scraper1 = BooksScraper("https://books.toscrape.com/catalogue/category/books/fiction_10/index.html")
    books_scraper1.extract_all_pages()
    books_scraper1.save_to_json()
    print("All book data saved to 'books_data.json'.")
    print(f"Total number of books: {len(books_scraper1.book_data)}")
