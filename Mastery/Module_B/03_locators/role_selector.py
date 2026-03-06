from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://github.com/login")

    username = page.get_by_role("textbox", name="Username")

    password = page.get_by_role("textbox", name="Password")

    button = page.get_by_role("button", name="Sign in")

    print(username)
    print(password)
    print(button)

    browser.close()