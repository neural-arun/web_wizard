import asyncio
import logging
import aiohttp

logging.basicConfig(level=logging.INFO)

async def fetch_html(url):
    timeout = aiohttp.ClientTimeout(total=10)# infinite wait se bachna

    async with aiohttp.ClientSession(timeout=timeout) as session:

        try:
            async with session.get(url) as response:
                logging.info(f"status: {response.status} for {url}")

                if response.status == 200:
                    return await response.text()
                elif response.status == 403:
                    logging.error(f"blocked by server: {url}")
                    return None
                elif response.status == 429:
                    logging.error(f"Too many requests: {url}")
                    return None
                else:
                    logging.error(f"unexpected error: {url}")
                    return None
                
        except asyncio.TimeoutError:
            logging.error("request timed out.")
            return None

async def main():
    html = await fetch_html("https://example.com")
    print("html is recieved ", html is not None)

asyncio.run(main())