from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://books.toscrape.com")

    title = page.locator("article.product_pod h3 a").first.get_attribute("title")

    price = page.locator(".price_color").first.inner_text()

    link = page.locator("article.product_pod h3 a").first.get_attribute("href")

    print(title)
    print(price)
    print(link)

    browser.close()