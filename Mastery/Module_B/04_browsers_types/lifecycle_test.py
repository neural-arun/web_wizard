import asyncio
from playwright.async_api import async_playwright

async def main():
    print("Starting Playwright")

    async with async_playwright() as p:
        print("Launching Browser")
        browser = await p.chromium.launch(headless=False)

        print("Creating Context")
        context = await browser.new_context()

        print("Opening Page")
        page = await context.new_page()

        await page.goto("https://example.com")
        print("Title:", await page.title())

        print("Closing Context")
        await context.close()

        print("Closing Browser")
        await browser.close()

    print("Playwright Closed")

asyncio.run(main())