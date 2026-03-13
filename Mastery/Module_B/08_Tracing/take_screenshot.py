from pathlib import Path

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    screenshot_path = Path(__file__).with_name("example2.png")
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com")
    page.get_by_role("link", name="Learn more").click()
    page.wait_for_load_state("load")
    page.screenshot(path=str(screenshot_path), full_page=True)

    browser.close()
