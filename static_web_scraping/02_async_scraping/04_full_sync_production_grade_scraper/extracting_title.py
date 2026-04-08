from bs4 import BeautifulSoup
from typing import Optional
import requests

response = requests.get("https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/").text


def extract_title(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")

    h1 = soup.find("h1")
    if not h1:
        return None

    title = h1.get_text(strip=True)
    if not title:
        return None

    return title

title = extract_title(response)

print(title)