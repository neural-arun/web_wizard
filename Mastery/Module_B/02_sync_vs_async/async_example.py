import asyncio
from playwright.async_api import async_playwright

async def scrape(page, url):
    await page.goto(url)
    print(await page.title())

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        tasks = []
        for _ in range(5):
            page = await browser.new_page()
            tasks.append(scrape(page, "https://example.com"))
        await asyncio.gather(*tasks)

asyncio.run(main())