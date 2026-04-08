

import asyncio
import aiohttp

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

# yahan sirf fetch_html ka skeleton

async def fetch_html(session,url,sem):
    try:
        async with sem:
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                return await response.text()
    except asyncio.TimeoutError:
        return None
    except aiohttp.ClientError:
        return None
    
async def main():
    sem = asyncio.Semaphore(3)
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        html_str_as_list = []
        tasks = []
        for url in urls:
            task = fetch_html(session,url,sem)
            tasks.append(task)
        html_str_as_list = await asyncio.gather(*tasks,return_exceptions=True)
        print(len(html_str_as_list))
        return html_str_as_list
result = asyncio.run(main())
success = sum(1 for r in result if isinstance(r, str))
failed = sum(1 for r in result if r is None)

print(f"Success: {success}, Failed: {failed}")
