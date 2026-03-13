# click a button.
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com")

    with page.expect_navigation():
        page.get_by_role("link", name="Learn more").click()

    print(page.title())
    browser.close()
