from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://duckduckgo.com")

    search_input = page.locator("input[name='q']")
    search_input.type("AI agents")
    search_input.press("Enter")

    results = page.locator("[data-testid='result-title-a']")
    results.first.wait_for()

    for i in range(min(5, results.count())):
        print(results.nth(i).inner_text())

    browser.close()
