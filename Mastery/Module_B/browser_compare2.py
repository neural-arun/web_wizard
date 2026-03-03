import asyncio
import time
from playwright.async_api import async_playwright

async def test_browser(p, engine_name, url="https://example.com"):
    browser = await getattr(p, engine_name).launch(headless=False)
    page = await browser.new_page()

    start = time.perf_counter()
    await page.goto(url, wait_until="load")
    load_time = time.perf_counter() - start

    title = await page.title()
    print(f"{engine_name:<9} | title: {title} | load time: {load_time:.3f} seconds")

    await browser.close()
    return load_time

async def main():
    results = {}
    async with async_playwright() as p:
        for engine in ["chromium", "firefox", "webkit"]:
            results[engine] = await test_browser(p, engine)

    print("\nSummary:")
    for engine, t in results.items():
        print(f"{engine:<9}: {t:.3f} seconds")

asyncio.run(main())
