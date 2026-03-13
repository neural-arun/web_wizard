from playwright.sync_api import sync_playwright  # Import Playwright's sync API helper.


def log_request(request):  # Define a function to handle each network request.
    print(f"{request.method} {request.url}")  # Print the request method and URL.


with sync_playwright() as p:  # Start Playwright and store the controller in p.
    browser = p.chromium.launch(headless=False)  # Launch a visible Chromium browser.
    page = browser.new_page()  # Open a new browser tab.

    page.on("request", log_request)  # Listen for every outgoing network request.
    page.goto("https://news.ycombinator.com")  # Open Hacker News in the browser.

    browser.close()  # Close the browser after the page finishes loading.
