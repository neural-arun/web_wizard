from playwright.sync_api import sync_playwright


with sync_playwright as p:
    browser = p.chromium.launch(headless=False)
    iphone = p.devices["iPhone 13"]

    context = browser.new_context(
        **iphone,
        locale="en-US",
        timezone_id="America/New_York",
        geolocation={"latitude":40.7128,"longitude":-74.0060},
        permissions=["geolocation"]
    )