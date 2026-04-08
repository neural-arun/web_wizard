from bs4 import BeautifulSoup
from typing import Optional
import requests

response = requests.get("https://blog.cloudflare.com/uk-google-ai-crawler-policy/").text

from bs4 import BeautifulSoup
from typing import Optional


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


article_text = extract_article_text(response)
print(article_text)