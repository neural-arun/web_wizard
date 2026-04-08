import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import Optional
import json
from pathlib import Path
import logging
import time
BASE_DIR = Path(__file__).parent
url_file = BASE_DIR/"data"/"urls.json"

BATCH_DIR = BASE_DIR / "data" / "batches"
BATCH_DIR.mkdir(parents=True, exist_ok=True)

# basic logger setup.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)




def load_urls():
    with open (url_file,"r",encoding="utf-8") as f:
        return json.load(f)

async def fetch_html(session,url,sem):
    start = time.perf_counter()
    logger.info(f"start {url}")
    try:
        async with sem:
            async with session.get(url) as response:
                
                if response.status != 200:
                    logger.warning(f"FAIL   {url} | status={response.status}")
                    return None
                await asyncio.sleep(1)
                return await response.text()
        
    except aiohttp.ClientError as e:
        logger.error(f"ERROR  {url} | {e}")
        return None
    finally:
        end = time.perf_counter()
        logger.info(f"END    {url} | {end - start:.2f}s")

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


# def extract_article_text(html: str) -> Optional[str]:
#     soup = BeautifulSoup(html, "lxml")

#     article = soup.find("article")
#     if not article:
#         return None

#     section = article.find("section")
#     if not section:
#         return None

#     parts: list[str] = []

#     for tag in section.find_all(["p", "h1", "h2", "h3"], recursive=True):
#         text = tag.get_text(strip=True)
#         if text:
#             parts.append(text)

#     if not parts:
#         return None

#     return "\n\n".join(parts)

def batch_urls(urls,batch_size):
    
    return [urls[i: i + batch_size] for i in range(0,len(urls),batch_size)]

async def scrape_article(session,article_url,sem):
    html = await fetch_html(session,article_url,sem)
    if not html:
        return None
    
    
    return {
        "url": article_url,
        "title": extract_title(html),
        "publish_date": extract_publish_date(html),
        "authors": extract_authors(html),
        
    }

async def main():
    urls = load_urls()
    batches = batch_urls(urls,100)

    sem = asyncio.Semaphore(5)

    async with aiohttp.ClientSession() as session:
        for batch_index, batch in enumerate(batches, start=1):
            logger.info(
                f"Starting batch {batch_index}/{len(batches)} "
                f"({len(batch)} URLs)"
            )

            tasks = [
                scrape_article(session, url, sem)
                for url in batch
            ]

            results = await asyncio.gather(*tasks)
            results = [r for r in results if r is not None]

            # ✅ SAVE THIS BATCH
            batch_file = BATCH_DIR / f"batch_{batch_index:03}.json"
            with open(batch_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            logger.info(
                f"Finished batch {batch_index} | "
                f"saved={len(results)} articles"
            )

            # polite pause
            await asyncio.sleep(1)

    logger.info("ALL batches completed")


start_time = time.perf_counter()
asyncio.run(main())
end_time = time.perf_counter()
print(f"ASYNC TIME: {end_time - start_time:.2f} seconds")