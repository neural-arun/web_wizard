import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

URL_FILE = DATA_DIR / "urls.json"

def collect_article_urls(base_url: str) -> list[str]:
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(base_url,headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    article_urls = set()
    articles = soup.find_all("article")

    for article in articles:
        first_div = article.find("div")
        if not first_div:
            continue
        first_a = first_div.find("a")
        if not first_a:
            continue

        href = first_a.get("href")
        if not href:
            continue

        full_url = urljoin(base_url,href)
        article_urls.add(full_url)
    print(f"Collected {len(article_urls)} URLs from {base_url}")
    return list(article_urls)

def collect_all_articles_urls():
    all_urls = set()
    for page_num in range(1,172):
        if page_num == 1:
            page_url = "https://blog.cloudflare.com/"
        else:
            page_url = f"https://blog.cloudflare.com/page/{page_num}/"
        try:
            page_urls = collect_article_urls(page_url)
        except requests.RequestException:
            print(f"Failed page {page_num}, skipping")
            continue
        all_urls.update(page_urls)
        print(f"page {page_num}: {len(page_urls)} URLs")

    return list(all_urls)


if __name__ == "__main__":
    urls = collect_all_articles_urls()

    with open(URL_FILE, "w", encoding="utf-8") as f:
        json.dump(urls, f, indent=2)

    print(f"Saved {len(urls)} URLs → {URL_FILE}")
    