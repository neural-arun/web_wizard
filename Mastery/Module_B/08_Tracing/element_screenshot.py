from pathlib import Path

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    screenshot_path = Path(__file__).with_name("h1.png")
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com")
    page.locator("a").click()
    page.wait_for_load_state("load")

    heading = page.locator("h1")
    heading.screenshot(path=str(screenshot_path))

    browser.close()
