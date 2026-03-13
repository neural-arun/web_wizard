from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.wikipedia.org")

    english_link = page.locator("#js-link-box-en")
    english_link.hover()
    english_link.click()

    print(page.title())
    browser.close()
