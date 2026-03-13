from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Launch browser in non-headless mode to see the actions
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Open Google
        page.goto("https://www.google.com")
        
        # Fill the search box with "AI healthcare"
        # Google's search input typically has the name attribute "q"
        page.fill("[name='q']", "AI healthcare ")
        
        # Press Enter to search
        page.keyboard.press("Enter")
        
        # Wait a few seconds to see the results before closing
        page.wait_for_timeout(5000)
        
        browser.close()

if __name__ == "__main__":
    main()
