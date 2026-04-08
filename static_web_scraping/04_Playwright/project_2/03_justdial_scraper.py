from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import time
import pathlib
import json

script_dir = pathlib.Path(__file__).parent.resolve()

def scrape_justdial(city="Delhi", category="Dentists", max_scrolls=5):
    extracted_data = []
    
    # --- THE ULTIMATE ANTI-BOT FIX: Stealth Injection V2 ---
    # In V2, Stealth wraps the entire Playwright instance!
    with Stealth().use_sync(sync_playwright()) as p:
        print("🚀 Launching Headful Chromium with Stealth Plugin...")
        # Add custom args to remove the "Chrome is being controlled by automated test software" banner
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        ) 
        
        # We add some stealth configurations
        # Bypassing bot detection often requires spoofing a real screen size and user-agent
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True,
            bypass_csp=True
        )
        page = context.new_page()
        
        # --- SPEED OPTIMIZATION 1: Request Interception ---
        # Stop downloading images, fonts, and media. 
        # CRITICAL FIX: We MUST allow 'stylesheet' (CSS), because Justdial uses CSS layouts 
        # to trigger IntersectionObservers for lazy-loading. Without CSS, infinite scroll breaks!
        def block_aggressively(route):
            if route.request.resource_type in ["image", "media", "font"]:
                route.abort()
            else:
                route.continue_()
        
        page.route("**/*", block_aggressively)

        target_url = f"https://www.justdial.com/{city}/{category}"
        print(f"🌍 Navigating to {target_url} ...")
        
        retry_count = 0
        while retry_count < 3:
            try:
                # We wait for the 'domcontentloaded' state because blocking images breaks 'load'
                page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
                break
            except Exception as e:
                print(f"Navigation timeout, retrying... ({retry_count}/3)")
                retry_count += 1
                
        print("✅ Page Loaded. Handling Pagination (Infinite Scroll)...")
        
        # --- FIX: We MUST guarantee the first batch of cards exist before we start fast-scrolling
        print("Waiting for initial cards to render in the DOM...")
        try:
            page.wait_for_selector('.resultbox_info', timeout=15000)
            previous_count = len(page.locator(".resultbox_info").all())
            print(f"Initial cards loaded: {previous_count}")
        except:
            print("❌ Failed to load any initial cards. Justdial might be blocking us heavily.")
            previous_count = 0

        # --- PAGINATION LOGIC (The Playwright Way) ---
        # Justdial doesn't have a "Next" button. It uses "Infinite Scroll".
        
        # 1. Bring the mouse into the center of the page so scrolling targets the main container
        page.mouse.move(500, 500)
        
        for i in range(max_scrolls):
            print(f"📜 Scrolling batch {i+1} of {max_scrolls}...")
            
            # --- ADVANCED ANTI-BOT FIX: True Mouse Scrolling ---
            # 2. Use the native OS-level mouse wheel to scroll down smoothly
            # This triggers the exact same events as a real human rolling a mouse wheel
            page.mouse.wheel(0, 3000)
            
            # --- SPEED OPTIMIZATION 2: Smart Waiting ---
            # Do NOT use wait_for_timeout(2500) recursively. If the data loads in 0.1s, we waste 2.4s.
            # Instead, we tell Playwright: "Wait exactly until the total number of cards increases"
            try:
                page.wait_for_function(f"document.querySelectorAll('.resultbox_info').length > {previous_count}", timeout=8000)
                # Give it exactly 0.5s to finish rendering the text tags inside the boxes
                page.wait_for_timeout(500)
                # Update our count for the next loop
                previous_count = len(page.locator(".resultbox_info").all())
            except:
                print("⚠️ No more new cards loaded or timeout reached. Stopping scroll.")
                break

        print("\n🔍 Extracting Data using your Locators...\n")

        # 1. Grab ALL the outer cards you found!
        # page.locator() returns a list of elements if it finds multiple matches
        cards = page.locator(".resultbox_info").all()
        
        print(f"Found {len(cards)} Business Cards on the screen.")
        
        # Loop through every massive card
        for card in cards:
            try:
                # Inside the card, look for the title you found.
                # Use .inner_text() to grab the human-readable text out of the HTML tag
                name = card.locator(".resultbox_title_anchor").inner_text(timeout=1000)
            except:
                name = "N/A"
                
            try:
                # Same thing for phone and rating
                phone = card.locator(".callcontent").inner_text(timeout=1000)
            except:
                phone = "N/A"
                
            try:
                rating = card.locator(".resultbox_totalrate").inner_text(timeout=1000)
            except:
                rating = "N/A"
                
            if name != "N/A":
                business = {
                    "Name": name,
                    "Phone": phone,
                    "Rating": rating
                }
                extracted_data.append(business)
                print(f"Extracted: {business['Name']} | ⭐ {business['Rating']} | 📞 {business['Phone']}")

        print("\n🛑 Closing browser...")
        context.close()
        browser.close()
        
    # Save the data
    save_path = script_dir / f"{city}_{category}_data.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)
        
    print(f"\n🎉 Successfully scraped {len(extracted_data)} local businesses.")
    print(f"💾 Saved to {save_path}")

if __name__ == "__main__":
    scrape_justdial(city="Delhi", category="Tech shops", max_scrolls=100)
