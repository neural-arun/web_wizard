from playwright.sync_api import sync_playwright
# sync_playwright main single thread insaan hoon ek kaam ek time pr.

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)   # chrome khol bhai.
    page = browser.new_page()    # ek naya tab de
    page.goto("https://example.com")
    page.wait_for_timeout(5000)
    print(page.title())
