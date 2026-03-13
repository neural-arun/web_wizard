from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/js")

    page.wait_for_selector(".quote")
    first_quote = page.locator(".quote .text").first.inner_text()
    print(first_quote)

    browser.close()

