from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    print(list(playwright.devices.keys()))
