import asyncio
import aiohttp
import logging
logging.basicConfig(
    level=logging.INFO,
    
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.get_logger(__name__)

async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
        except asyncio.TimeoutError:
            logger.error(f"[Network error]: {url}")
            return None
        except aiohttp.ClientError as e:
            logger.error(f"[Network Error] {e} for {url}")
            return None
            
async def main():
    await fetch_html("https://example.com")
asyncio.run(main())