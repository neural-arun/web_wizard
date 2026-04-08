import aiohttp
import asyncio
import json
import pathlib
from bs4 import BeautifulSoup

script_dir = pathlib.Path(__file__).parent.resolve()

async def fetch_justdial_api(city="Delhi", category="Tech shops", num_pages=15):
    # This is the exact URL we intercepted from the backend!
    url = f"https://www.justdial.com/api/resultsPageFooterData?searchReferer=genReferer=gen"
    extracted_data = []
    
    # We forge the exact headers a browser sends
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://www.justdial.com",
        "Referer": f"https://www.justdial.com/{city}/{category}"
    }
    
    print(f"🕵️ Bypassing Browser. Hitting API directly for {city} {category}...\n")
    
    async with aiohttp.ClientSession(headers=headers) as session:
        for page_num in range(1, num_pages + 1):
            # This is the intercepted payload from our Playwright script!
            payload = {
                "area": "",
                "catname": category,
                "city": city,
                "ncatid": 11216691, # The internal ID we found
                "pg_no": str(page_num),
                "searchTerm": category.replace(" ", "%20")
            }
            
            try:
                # We POST directly to their backend
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Justdial sometimes returns raw HTML strings inside their JSON (ugh!)
                        # We use BeautifulSoup just to parse the text out of those strings
                        if 'results' in data and data['results']:
                            html_chunk = data['results']
                            soup = BeautifulSoup(html_chunk, 'html.parser')
                            
                            cards = soup.select(".resultbox_info")
                            print(f"✅ Page {page_num}: Found {len(cards)} items.")
                            
                            for card in cards:
                                try:
                                    name_tag = card.select_one(".resultbox_title_anchor")
                                    name = name_tag.text.strip() if name_tag else "N/A"
                                    
                                    phone_tag = card.select_one(".callcontent")
                                    phone = phone_tag.text.strip() if phone_tag else "N/A"
                                    
                                    rating_tag = card.select_one(".resultbox_totalrate")
                                    rating = rating_tag.text.strip() if rating_tag else "N/A"
                                    
                                    if name != "N/A":
                                        extracted_data.append({
                                            "Name": name, "Phone": phone, "Rating": rating
                                        })
                                except Exception as e:
                                    pass
                                    
                    else:
                        print(f"❌ Page {page_num} failed with status {response.status}")
                        break
                        
            except Exception as e:
                print(f"❌ Error on page {page_num}: {e}")
                
            # Be polite to the API so we don't get IP banned immediately
            await asyncio.sleep(1)

    # Save the data
    save_path = script_dir / f"{city}_{category}_API_data.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)
        
    print(f"\n🎉 BOOM! Extracted {len(extracted_data)} local businesses via API.")
    print(f"💾 Saved to {save_path}")

if __name__ == "__main__":
    asyncio.run(fetch_justdial_api(city="Delhi", category="Tech shops", num_pages=20))
