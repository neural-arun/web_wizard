import asyncio
import time
from playwright.async_api import async_playwright

async def test_browser(engine_name):
    async with async_playwright() as p:
        browser = await getattr(p, engine_name).launch(headless=False)
        page = await browser.new_page()
        start = time.time()
        await page.goto("https://example.com")
        end = time.time()
        print(f"{engine_name} title:", await page.title())
        await browser.close()

async def main():
    for engine in ["chromium", "firefox", "webkit"]:
        await test_browser(engine)
        print

asyncio.run(main())