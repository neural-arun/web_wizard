# FAILED PRACTICE:


"""
👉 Ek simple async script likho:

5 URLs

Single ClientSession

fetch_html
"""
import asyncio
import aiohttp
htmls = []
async def fetch_html(session,url):
    async with session.get(url) as response:
        return await response.text()


async def main(urls):
    async with aiohttp.ClientSession(
         timeout=10
    ) as session:
        for url in urls:
            await htmls.append(fetch_html(session,url))
            print(f"returning html of url: {url}")

        return await htmls
urls = [
    "https://example.com",
"https://httpbin.org/html",
"https://quotes.toscrape.com",
"https://books.toscrape.com",
"https://news.ycombinator.com",
"https://jsonplaceholder.typicode.com/posts",
"https://jsonplaceholder.typicode.com/users",
"https://www.wikipedia.org",
"https://httpbin.org/delay/2",
"https://httpbin.org/headers",

]
asyncio.run(main=main(urls))

# 