import requests
import time
import logging
import json
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Optional

# ---------------- LOGGER ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------- PATH SETUP ----------------
BASE_DIR = Path(__file__).parent
URL_FILE = BASE_DIR / "data" / "urls.json"

# ---------------- LOAD URLS ----------------
def load_urls():
    with open(URL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------- FETCH HTML (SYNC) ----------------
def fetch_html_sync(url):
    start = time.perf_counter()
    logger.info(f"START {url}")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            logger.warning(f"FAIL {url} | status={response.status_code}")
            return None

        # Match async delay for fair comparison
        time.sleep(1)

        return response.text

    except requests.RequestException as e:
        logger.error(f"ERROR {url} | {e}")
        return None

    finally:
        end = time.perf_counter()
        logger.info(f"END {url} | {end - start:.2f}s")

# ---------------- PARSING FUNCTIONS ----------------
def extract_title(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")

    h1 = soup.find("h1")
    if not h1:
        return None

    title = h1.get_text(strip=True)
    return title if title else None


def extract_publish_date(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")

    article = soup.find("article")
    if not article:
        return None

    p = article.find("p")
    if not p:
        return None

    date_text = p.get_text(strip=True)
    return date_text if date_text else None


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

# ---------------- SCRAPE ONE ARTICLE ----------------
def scrape_article_sync(url):
    html = fetch_html_sync(url)
    if not html:
        return None

    return {
        "url": url,
        "title": extract_title(html),
        "publish_date": extract_publish_date(html),
        "authors": extract_authors(html),
    }

# ---------------- MAIN ----------------
def main():
    urls = load_urls()

    logger.info(f"Loaded {len(urls)} URLs")

    start_total = time.perf_counter()

    results = []
    for url in urls:
        r = scrape_article_sync(url)
        if r:
            results.append(r)

    end_total = time.perf_counter()

    # Pretty print results
    for r in results:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        print("=" * 70)

    print(f"\nTotal articles scraped: {len(results)}")
    print(f"SYNC TOTAL TIME: {end_total - start_total:.2f}s")


# ---------------- ENTRY ----------------
if __name__ == "__main__":
    main()
