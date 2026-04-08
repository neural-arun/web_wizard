import time
import requests

URLS = [
    "https://example.com",
    "https://example.com",
    "https://example.com",
]

last_time = None
session = requests.Session()

print("\n=== SCRAPER HEALTH CHECK ===\n")

for i, url in enumerate(URLS, start=1):
    now = time.time()

    gap = None if last_time is None else round(now - last_time, 2)

    response = session.get(url)

    print(f"Request #{i}")
    print("Status Code:", response.status_code)
    print("Response Size:", len(response.text))
    print("Gap from last request:", "FIRST" if gap is None else f"{gap}s")

    print("Headers Summary:")
    print({
        "User-Agent": response.request.headers.get("User-Agent"),
        "Header-Count": len(response.request.headers),
    })

    print("Cookies Present:", bool(session.cookies))
    print("-" * 40)

    last_time = now
