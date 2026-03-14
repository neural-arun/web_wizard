from pathlib import Path

from playwright.sync_api import sync_playwright


with sync_playwright() as playwright:
    screenshot_path = Path(__file__).with_name("mobile.png")
    browser = playwright.chromium.launch()
    context = browser.new_context(viewport={"width": 375, "height": 667})

    page = context.new_page()
    page.goto("https://news.ycombinator.com")
    page.screenshot(path=str(screenshot_path))

    browser.close()
