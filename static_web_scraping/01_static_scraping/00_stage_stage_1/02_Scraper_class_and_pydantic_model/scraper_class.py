import requests
from bs4 import BeautifulSoup

class QuoteScraper:
    def __init__(self,base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
            }
        
    def fetch_url(self,url):
        response = requests.get(url,headers=self.headers)
        return response.text
    
    def parse_html(self,html):
        return BeautifulSoup(html,"lxml")
    
    def extract_quotes(self,soup):
        quotes_data = []

        quotes = soup.find_all("div",class_="quote")

        for quote in quotes:
            text = quote.find("span", class_="text").get_text()
            author = quote.find("small", class_="author").get_text()
            tags = quote.find_all("a", class_="tag")
            tag_texts = [tag.get_text() for tag in tags]

            quotes_data.append({
                "text": text,
                "author": author,
                "tags": tag_texts
            })

        return quotes_data
        
    def scrape_all_pages(self):
        current_url = self.base_url
        all_quotes = []

        while True:
            html = self.fetch_url(current_url)
            soup = self.parse_html(html)
            page_quotes = self.extract_quotes(soup)
            all_quotes.extend(page_quotes)

            next_button = soup.find("li", class_="next")
            if next_button is None:
                break

            next_link = next_button.find("a")["href"]
            current_url = self.base_url+next_link
        
        return all_quotes
    

if __name__ == "__main__":
    scraper = QuoteScraper("https://quotes.toscrape.com/")
    data = scraper.scrape_all_pages()

    print(f"Total quotes: {len(data)}")