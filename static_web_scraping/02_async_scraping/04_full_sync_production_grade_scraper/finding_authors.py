from bs4 import BeautifulSoup

import requests

response = requests.get("https://blog.cloudflare.com/vertical-microfrontends/").text



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
writers = extract_authors(response)
print(writers)