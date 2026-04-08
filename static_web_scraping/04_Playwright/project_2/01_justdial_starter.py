from playwright.sync_api import sync_playwright

def run_scraper():
    # We use 'with' so that Playwright automatically cleans up and closes when we are done
    with sync_playwright() as p:
        # 1. Launch the Browser (The engine)
        # We explicitly set headless=False so you can see what is happening!
        print("🚀 Launching Chromium Browser...")
        browser = p.chromium.launch(headless=False)

        # 2. Create the Context (The Incognito window)
        print("🕵️  Creating an isolated browser context...")
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )

        # 3. Open a New Tab (The Page)
        print("📄 Opening new tab...")
        page = context.new_page()

        # 4. Navigate to Justdial (Wait until the DOM is loaded)
        target_url = "https://www.justdial.com/Delhi/Dentists"
        print(f"🌍 Navigating to {target_url} ...")
        
        # We wait for the 'domcontentloaded' state so we know the basic HTML is there
        page.goto(target_url, wait_until="domcontentloaded")
        
        print("\n✅ Navigation complete!")
        print("⏸️ Pausing execution so you can inspect the data...")
        
        # THIS IS THE MAGIC COMMAND FOR LEARNING:
        # It pauses the script and opens the Playwright Inspector so you can point-and-click
        # on elements to find the correct CSS Selectors (Locators).
        page.pause()
        
        # ---------------------------------------------------------
        # (This section will run AFTER you click 'Resume' in the Inspector)
        print("\n🛑 Closing browser...")
        context.close()
        browser.close()

if __name__ == "__main__":
    run_scraper()
