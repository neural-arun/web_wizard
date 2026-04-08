import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://example.com/")
    page.get_by_role("link", name="Learn more").click()
    page.get_by_role("link", name="IANA-managed Reserved Domains").click()
    page.get_by_role("link", name="RFC 2606").click()
    page.get_by_role("link", name="View errata").click()
    page.get_by_role("link", name="Source of RFC").nth(2).click()
    
    page.get_by_role("link", name="Erratum ID 1504").click()
    page.get_by_role("link", name="Document Retrieval").click()
    page.get_by_role("link", name="Format Change FAQ").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
