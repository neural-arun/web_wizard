import asyncio
import aiohttp
import pathlib
import json
import time

# Get the directory where this script is located
script_dir = pathlib.Path(__file__).parent.resolve()

# The headers we found in DevTools
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}
BASE_URL = "https://api.hm.com/search-services/v1/en_in/listing/resultpage"

async def fetch_page(session, page_num):
    """Fetches a single page of data from the API asynchronously."""
    params = {
        "pageSource": "PLP",
        "page": page_num, 
        "sort": "RELEVANCE",
        "pageId": "/men/shop-by-product/view-all",
        "page-size": 36,
        "categoryId": "men_viewall",
        "filters": "sale:false||oldSale:false",
        "touchPoint": "DESKTOP",
        "skipStockCheck": "false"
    }

    print(f"🚀 Requesting Page {page_num}...")
    
    try:
        async with session.get(BASE_URL, params=params, headers=HEADERS) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"❌ Failed on Page {page_num} - Status: {response.status}")
                return None
    except Exception as e:
        print(f"⚠️ Error on Page {page_num}: {e}")
        return None

async def main():
    start_time = time.time()
    
    # Looking at your hm_page_1.json, line 7 shows "totalPages": 72
    total_pages_to_scrape = 72 # Let's do 5 pages first so we don't hammer their server immediately. Change this to 72 if you want it all!
    all_extracted_products = []
    
    # Create the Async Session
    async with aiohttp.ClientSession() as session:
        # 1. We create a list of "tasks" (promises to fetch each page)
        tasks = []
        for i in range(1, total_pages_to_scrape + 1):
            tasks.append(fetch_page(session, i))
            
        # 2. We run all tasks CONCURRENTLY using asyncio.gather
        print(f"⚡ Launching {total_pages_to_scrape} concurrent API requests...")
        results = await asyncio.gather(*tasks)
        
        # 3. Process the results when they all return
        for index, data in enumerate(results):
            if data:
                page_num = index + 1
                products = data.get("plpList", {}).get("productList", [])
                
                print(f"✅ Page {page_num} returned {len(products)} products.")
                
                for item in products:
                    name = item.get("productName", "Unknown")
                    
                    # Safer extraction in case 'prices' array is empty on some items
                    price = "Unknown"
                    price_list = item.get("prices", [])
                    if len(price_list) > 0:
                        price = price_list[0].get("price", "Unknown")
                        
                    all_extracted_products.append({
                        "name": name,
                        "price": price,
                        "page_found": page_num
                    })

    # Save everything cleanly to a single JSON file
    save_path = script_dir / "all_hm_products.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(all_extracted_products, f, indent=4)
        
    end_time = time.time()
    print(f"\n🎉 SUCCESS! Extracted {len(all_extracted_products)} total products in {round(end_time - start_time, 2)} seconds.")
    print(f"💾 Saved to {save_path}")

if __name__ == "__main__":
    # Windows-specific fix for asyncio Event Loop policy
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())
