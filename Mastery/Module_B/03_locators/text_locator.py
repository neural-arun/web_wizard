from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://example.com")

    # 1 title print
    print(page.title())

    # 2 link click
    page.get_by_text("Learn more").click()

    browser.close()