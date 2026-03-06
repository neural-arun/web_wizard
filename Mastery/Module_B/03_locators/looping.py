from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://news.ycombinator.com")

    titles = page.locator(".titleline a")

    for i in range(10):

        title = titles.nth(i).inner_text()

        link = titles.nth(i).get_attribute("href")

        print(title)
        print(link)
        print("-----")

    browser.close()