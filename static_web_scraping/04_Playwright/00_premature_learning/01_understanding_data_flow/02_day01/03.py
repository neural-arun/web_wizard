import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://example.com/")
    page.get_by_role("link", name=re.compile("Learn", re.I)).click()
    page.get_by_role("link", name="IANA-managed Reserved Domains").click()
    page.get_by_role("link", name="XN--11B5BS3A9AJ6G").click()
    page.wait_for_load_state("networkidle")

    print("Current URL:", page.url)
    print("Page Title:", page.title())
    # -------------------------------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
