import asyncio
from playwright.async_api import async_playwright

step = 0
def log(msg):
    global step
    step += 1
    print(f"[{step:02}] {msg}")

async def open_pages_in_context(context, context_name):
    pages = []
    for i in range(1, 3):  # 2 pages per context
        log(f"{context_name}: creating page {i}")
        page = await context.new_page()
        pages.append(page)

        log(f"{context_name}: page {i} -> goto example.com")
        await page.goto("https://example.com")
        title = await page.title()
        log(f"{context_name}: page {i} title = {title}")

    return pages

async def main():
    log("Starting Playwright")
    async with async_playwright() as p:
        log("Launching Browser")
        browser = await p.chromium.launch(headless=False)

        log("Creating Context 1")
        context1 = await browser.new_context()

        log("Creating Context 2")
        context2 = await browser.new_context()

        # Sequential opening (easy to follow lifecycle order)
        pages_c1 = await open_pages_in_context(context1, "Context-1")
        pages_c2 = await open_pages_in_context(context2, "Context-2")

        # Explicit close order
        for i, page in enumerate(pages_c1, 1):
            log(f"Context-1: closing page {i}")
            await page.close()

        for i, page in enumerate(pages_c2, 1):
            log(f"Context-2: closing page {i}")
            await page.close()

        log("Closing Context 1")
        await context1.close()

        log("Closing Context 2")
        await context2.close()

        log("Closing Browser")
        await browser.close()

    log("Playwright Closed")

asyncio.run(main())
