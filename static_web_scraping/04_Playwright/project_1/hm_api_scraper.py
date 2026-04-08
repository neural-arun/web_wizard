import requests
import json
import time

def scrape_hm_api():
    base_url = "https://api.hm.com/search-services/v1/en_in/listing/resultpage"
    
    # We are using a dictionary to map out the exact URL parameters you found
    # This is much cleaner than building one massive, ugly string
    params = {
        "pageSource": "PLP",
        "page": 1,  # Let's start on page 1
        "sort": "RELEVANCE",
        "pageId": "/men/shop-by-product/view-all",
        "page-size": 36,
        "categoryId": "men_viewall",
        "filters": "sale:false||oldSale:false",
        "touchPoint": "DESKTOP",
        "skipStockCheck": "false"
    }

    # This is the secret handshake. Without this, H&M Server rejects you.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
    }

    print(f"🕵️  Sending Request to H&M API for Page {params['page']}...")
    
    # We pass the URL, our parameters, and our headers into the requests library
    response = requests.get(base_url, params=params, headers=headers)

    # Check if the server let us in (200 OK)
    if response.status_code == 200:
        print("✅ Access Granted! We found the JSON payload.")
        
        # Convert the raw text response into a Python dictionary
        data = response.json()
        
        # Let's extract the actual products from the JSON structure
        # (Looking at your screenshot, the products are likely inside an array, often called 'results', 'products', 'hits', or similar. 
        # H&M often puts them under a key like "plpList" or "products". We will print the keys first to see the exact structure)
        
        print("\nHere are the top-level keys in the JSON dictionary:")
        print(data.keys())
        
        import pathlib
        
        # Get the directory where this script is located
        script_dir = pathlib.Path(__file__).parent.resolve()
        save_path = script_dir / "hm_page_1.json"
        
        # Let's write the raw JSON to a file so we can inspect it safely
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        print(f"\n💾 Saved the full JSON response to '{save_path}' for you to explore!")

    else:
        print(f"❌ Access Denied. Status Code: {response.status_code}")
        print("Response Text:", response.text)

if __name__ == "__main__":
    scrape_hm_api()
