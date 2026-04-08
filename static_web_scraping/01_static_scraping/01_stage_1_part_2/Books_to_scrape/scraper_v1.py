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
        response = requests.get(url, headers=self.headers)
        response.encoding = "utf-8"
        return response.text

    
    def parse_html(self,html):
        return BeautifulSoup(html,"lxml")
    
    def extract_records(self,soup):
        
        records = soup.find_all("article",class_="product_pod")
        for record in records:
            title = record.find("h3").find("a")["title"]
            rating_tag = record.find("p",class_="star-rating")  # rating_tag is a tag object not a list.
            rating = rating_tag["class"][-1]
            # If you access rating_tag["class"], you get the list of class names:["star-rating", "Three"].
            price = record.find("p", class_="price_color").text.strip()
            availability = record.find("p", class_="instock").text.strip()

            one_book_data = {
                "Title": title,
                "Rating": rating,
                "Price": price,
                "Availability": availability
            }

            self.book_data.append(one_book_data)
    
    def extract_all_pages(self):
        current_url = self.base_url
        while True:
            html = self.fetch_html(current_url)
            soup = self.parse_html(html)
            self.extract_records(soup)
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
