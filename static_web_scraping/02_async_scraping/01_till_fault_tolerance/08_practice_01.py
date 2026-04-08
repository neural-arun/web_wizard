import asyncio
import aiohttp
async def fetch_status(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(url, response.status)

asyncio.run(fetch_status("https://www.linkedin.com/feed/"))