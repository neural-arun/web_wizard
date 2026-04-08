from playwright.sync_api import sync_playwright
import time
import json

def listen_to_traffic(city="Delhi", category="Tech shops"):
    print(f"🕵️ Starting API Interceptor for {city} {category}...\n")
    
    from playwright_stealth import Stealth
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        ) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True,
            bypass_csp=True
        )
        page = context.new_page()

        # 1. Block images/fonts (We want the network tab clean)
        def block_media(route):
            if route.request.resource_type in ["image", "media", "font"]:
                route.abort()
            else:
                route.continue_()
        page.route("**/*", block_media)

        # 2. Set up the Interceptor! 
        # Every time the page makes a background request, this function runs.
        def handle_response(response):
            # We only care about API calls (Fetch/XHR), not HTML documents
            if response.request.resource_type in ["fetch", "xhr"]:
                url = response.url
                # Filter out obvious junk (analytics, ads, tracking)
                if "google" not in url and "analytics" not in url:
                    print(f"\n🔗 [INTERCEPTED] {response.request.method} {url}")
                    
                    # Try to print the payload sent to the server (if it was a POST request)
                    post_data = response.request.post_data
                    if post_data:
                        try:
                            # Try to parse and format it nicely if it's JSON
                            parsed_data = json.loads(post_data)
                            print("📦 Payload Sent:")
                            print(json.dumps(parsed_data, indent=2))
                        except json.JSONDecodeError:
                            # If it's URL-encoded or raw text, just print it
                            print(f"📦 Raw Payload: {post_data}")

        # Attach our listener to the page
        page.on("response", handle_response)

        target_url = f"https://www.justdial.com/{city}/{category}"
        print(f"🌍 Navigating to {target_url} ...")
        
        try:
            page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        except Exception:
            print("Timeout on initial load, proceeding anyway...")

        print("✅ Waiting for Initial Load...")
        page.wait_for_timeout(3000)
        
        print("\n📜 Triggering a single scroll to force the API to fire...")
        page.mouse.move(500, 500)
        page.mouse.wheel(0, 3000)
        
        # Wait for the network requests to finish coming back
        page.wait_for_timeout(5000)
        
        print("\n🛑 Closing Interceptor. Check the terminal output above!")
        context.close()
        browser.close()

if __name__ == "__main__":
    listen_to_traffic()
