import requests
from bs4 import BeautifulSoup

class BooksScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
        }

    def fetch_html(self, url):
        response = requests.get(url, headers=self.headers)
        return response.text

    def parse_html(self, html_content):
        return BeautifulSoup(html_content, "lxml")

    def extract_data(self, soup):
        items = soup.find_all("article", class_="product_pod")
        for item in items:
            # Star rating
            rating = item.find("p", class_="star-rating")["class"][-1]
            
            # Name of the book
            title = item.find("h3").find("a")["title"]
            
            # Price
            price = item.find("p", class_="price_color").text
            
            # Availability
            availability = item.find("p", class_="instock availability").text.strip()
            
            print(f"Title: {title} | Rating: {rating} | Price: {price} | Status: {availability}")

    def extract_all_pages(self):
        current_url = self.base_url
        
        while True:
            html = self.fetch_html(current_url)
            soup = self.parse_html(html)
            self.extract_data(soup)
            
            # Pagination logic
            next_tag = soup.find("li", class_="next")
            if next_tag:
                next_link = next_tag.find("a")["href"]
                # Adjusting URL for relative paths if necessary
                if "catalogue/" not in next_link and "catalogue/" in self.base_url:
                    current_url = self.base_url.replace("index.html", "") + next_link
                else:
                    current_url = self.base_url.rsplit('/', 1)[0] + "/" + next_link
            else:
                break

# Example usage:
scraper = BooksScraper("https://books.toscrape.com/catalogue/page-1.html")
scraper.extract_all_pages()