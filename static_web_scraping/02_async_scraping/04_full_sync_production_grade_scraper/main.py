import requests
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup

def extract_title(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")

    h1 = soup.find("h1")
    if not h1:
        return None

    title = h1.get_text(strip=True)
    if not title:
        return None

    return title

def extract_publish_date(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")

    article = soup.find("article")
    if not article:
        return None

    p = article.find("p")
    if not p:
        return None

    date_text = p.get_text(strip=True)
    if not date_text:
        return None

    return date_text

def extract_authors(html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")

    article = soup.find("article")
    if not article:
        return []

    authors = []

    ul = article.find("ul")
    if not ul:
        return authors

    for li in ul.find_all("li"):
        div = li.find("div")
        if not div:
            continue

        a = div.find("a")
        if not a:
            continue

        name = a.get_text(strip=True)
        if name:
            authors.append(name)

    return authors


def extract_article_text(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")

    article = soup.find("article")
    if not article:
        return None

    section = article.find("section")
    if not section:
        return None

    parts: list[str] = []

    for tag in section.find_all(["p", "h1", "h2", "h3"], recursive=True):
        text = tag.get_text(strip=True)
        if text:
            parts.append(text)

    if not parts:
        return None

    return "\n\n".join(parts)

def scrape_article(article_url: str) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(article_url, timeout=10)
        if response.status_code != 200:
            return None
        html = response.text

        article_data = {
            "url": article_url,
            "title": extract_title(html),
            "publish_date": extract_publish_date(html),
            "authors": extract_authors(html),
            "article_text": extract_article_text(html),
        }

        return article_data
    except requests.RequestException:
        return None
    

def scrape_articles(urls: list[str]) -> list[dict]:
    results = []

    for url in urls:
        data = scrape_article(url)
        if data:
            results.append(data)

    return results

if __name__ == "__main__":
    urls = []
    

    articles = scrape_articles(urls)

    for article in articles:
        print("=" * 40)
        print("Title:", article["title"])
        print("Date:", article["publish_date"])
        print("Authors:", article["authors"])
        print("Text preview:", article["article_text"][:300])


