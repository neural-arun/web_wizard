import asyncio
from playwright.async_api import async_playwright

async def open_pages_in_context(context, context_name, urls):
    pages = []
    for i, url in enumerate(urls, 1):
        page = await context.new_page()
        await page.goto(url)
        print(f"{context_name} | Page {i} | {url} | Title: {await page.title()}")
        pages.append(page)
    return pages

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context1 = await browser.new_context()
        context2 = await browser.new_context()

        urls_context1 = [
            "https://example.com",
            "https://www.python.org",
        ]
        urls_context2 = [
            "https://playwright.dev",
            "https://github.com",
        ]

        pages_c1 = await open_pages_in_context(context1, "Context-1", urls_context1)
        pages_c2 = await open_pages_in_context(context2, "Context-2", urls_context2)

        for page in pages_c1 + pages_c2:
            await page.close()

        await context1.close()
        await context2.close()
        await browser.close()

asyncio.run(main())
