from playwright.sync_api import sync_playwright
import pathlib

script_dir = pathlib.Path(__file__).parent.resolve()

def extract_html():
    with sync_playwright() as p:
        print("🚀 Launching Chromium (Headful to bypass basic bot detection)...")
        # Justdial blocks headless browsers. We must use headful.
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        target_url = "https://www.justdial.com/Delhi/Dentists"
        print(f"🌍 Navigating to {target_url} ...")
        
        # Wait for the DOM, then sleep to let JS render the list
        page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        print("Waiting 3 seconds for JS render...")
        page.wait_for_timeout(3000)
        
        print("✅ Navigation complete! Extracting the entire page's HTML structure...")
        
        # Just grab the raw HTML of the body
        html_content = page.inner_html("body")
        
        save_path = script_dir / "justdial_raw.html"
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"💾 Saved the raw, JavaScript-rendered HTML to {save_path}")
        print("Now we can analyze the CSS classes safely without the website changing on us!")
        
        context.close()
        browser.close()

if __name__ == "__main__":
    extract_html()
