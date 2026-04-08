from bs4 import BeautifulSoup
from typing import Optional
import requests

response = requests.get("https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/").text

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

publish_date = extract_publish_date(response)

print(publish_date)