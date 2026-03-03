import asyncio
from playwright.async_api import async_playwright

semaphore = asyncio.Semaphore(3)  # limit concurrency

async def visit(p, url, idx):
    async with semaphore:
        print(f"Starting task {idx}")

        browser = p.chromium
        context = await browser.launch().new_context()
        page = await context.new_page()

        await page.goto(url)
        print(f"Task {idx} title:", await page.title())

        await context.close()
        print(f"Finished task {idx}")

async def main():
    async with async_playwright() as p:
        urls = ["https://example.com"] * 6
        tasks = [visit(p, url, i) for i, url in enumerate(urls)]
        await asyncio.gather(*tasks)

asyncio.run(main())