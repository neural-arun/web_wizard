import json
from playwright.sync_api import sync_playwright

new_york = {
    "latitude": 40.7128,
    "longitude": -74.0060,
}

with sync_playwright() as p:
    iphone_13 = p.devices["iPhone 13"]

    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        **iphone_13,
        locale="en-US",
        timezone_id="America/New_York",
        geolocation=new_york,
    )

    context.grant_permissions(["geolocation"], origin="https://httpbin.org")

    page = context.new_page()
    response = page.goto("https://httpbin.org/headers")

    headers = response.json()["headers"]
    print(json.dumps(headers, indent=4))

    browser.close()
