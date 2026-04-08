import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Function that collects article URLs from a given base page
def collect_article_urls(base_url: str) -> list[str]:

    # Send a GET request to the website
    response = requests.get(base_url, timeout=10)

    # If the request failed (404, 500, etc), stop immediately
    response.raise_for_status()

    # Parse the HTML content using lxml parser
    soup = BeautifulSoup(response.text, "lxml")

    # Empty list to store final article URLs
    article_urls = []

    # Find ALL <article> tags on the page
    articles = soup.find_all("article")

    # Loop through each article one by one
    for article in articles:

        # Inside the article, find the FIRST <div>
        first_div = article.find("div")
        if not first_div:
            continue  # skip this article if no div found

        # Inside that div, find the FIRST <a> tag
        first_a = first_div.find("a")
        if not first_a:
            continue  # skip if no link found

        # Extract the value of href attribute from <a>
        href = first_a.get("href")
        if not href:
            continue  # skip if href is missing

        # Convert relative URL to absolute URL
        full_url = urljoin(base_url, href)

        # Add the final URL to the list
        article_urls.append(full_url)

    # Return the collected list of article URLs
    return article_urls


# This block runs ONLY when the file is executed directly
if __name__ == "__main__":

    # Call the function with Cloudflare blog homepage
    urls = collect_article_urls("https://blog.cloudflare.com/")

    # Print how many URLs were collected
    print(f"Collected {len(urls)} article URLs")
    with open( BASE_DIR / "list_of_url.py", "w") as f:
        f.write("URLS = ")
        f.write(repr(urls))
        f.write("\n")
    
