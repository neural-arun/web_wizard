import time
import requests

urls = ["https://example.com"] * 5

last_request_time = None

for i, url in enumerate(urls, start=1):
    current_time = time.time()

    if last_request_time is None:
        gap = None
    
    else:
        gap = round(current_time - last_request_time, 2)

    response = requests.get(url)

    print(f"Request #{i}")
    print("Status Code:", response.status_code)
    print("Timestamp:", round(current_time, 2))

    if gap is None:
        print("Gap from last request: FIRST REQUEST")
    else:
        print("Gap from last request:", gap, "seconds")

    print("-" * 40)
    print(response.cookies)

    last_request_time = current_time
if not urls:
    print("❌ No URLs provided. Exiting.")
    exit()
