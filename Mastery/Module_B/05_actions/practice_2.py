from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Launch browser in non-headless mode to see the actions
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Open Wikipedia
        page.goto("https://www.wikipedia.org/")
        
        # Fill the search box with "bioinformatics"
        # Wikipedia's search input typically has the name attribute "search"
        page.fill("input[name='search']", "bioinformatics")
        
        # Press Enter to search
        page.keyboard.press("Enter")
        
        # Wait a few seconds to see the results before closing
        page.wait_for_timeout(5000)
        
        browser.close()

if __name__ == "__main__":
    main()
