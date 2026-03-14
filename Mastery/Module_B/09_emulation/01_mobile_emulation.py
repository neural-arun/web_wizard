# Import the sync Playwright API because this script should use the synchronous style.
from playwright.sync_api import sync_playwright


# Start Playwright so we can launch Chromium and use Playwright's built-in device settings.
with sync_playwright() as playwright:
    # Get the predefined iPhone 13 device profile to emulate its screen, touch support, and user agent.
    iphone_13 = playwright.devices["iPhone 13"]

    # Launch a Chromium browser instance.
    browser = playwright.chromium.launch(headless=False)

    # Create a browser context that behaves like an iPhone 13.
    context = browser.new_context(**iphone_13)

    # Open a new page inside the emulated mobile context.
    page = context.new_page()

    # Navigate to the target website.
    page.goto("https://example.com")

    # Print the page title to the terminal.
    print(page.title())

    # Close the browser after the work is done.
    browser.close()

