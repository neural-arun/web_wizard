import asyncio
from playwright.async_api import async_playwright

semaphore = asyncio.Semaphore(3)  # limit concurrent tasks

async def visit(browser, url, idx):
    async with semaphore:
        print(f"Starting task {idx}")

        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(url)
            print(f"Task {idx} title: {await page.title()}")
        finally:
            await context.close()
            print(f"Finished task {idx}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # launch once

        urls = ["https://example.com"] * 6
        tasks = [visit(browser, url, i) for i, url in enumerate(urls, start=1)]
        await asyncio.gather(*tasks)

        await browser.close()

asyncio.run(main())
