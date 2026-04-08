import time
import requests

urls = ["https://example.com"] * 20

for i, url in enumerate(urls, start=1):
    start = time.time()

    r = requests.get(url)

    elapsed = time.time() - start

    print(f"Request #{i}")
    print("Status:", r.status_code)
    print("Time taken:", round(elapsed, 2), "sec")
    print("-" * 30)
