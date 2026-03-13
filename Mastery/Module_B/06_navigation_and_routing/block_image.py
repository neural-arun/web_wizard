from playwright.sync_api import sync_playwright


def block_images(route):
    if route.request.resource_type == "image":
        route.abort()
    else:
        route.continue_()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.route("**/*", block_images)
    page.goto("https://wikipedia.org")

    print(page.title())
    browser.close()

