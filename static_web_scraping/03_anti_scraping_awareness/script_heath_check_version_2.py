import time
import requests

# =========================
# CONFIG (ONLY CHANGE THIS)
# =========================
URLS = [
    "https://example.com",
    "https://example.com",
    "https://example.com",
]

# =========================
# INTERNAL STATE
# =========================
last_request_time = None
session = requests.Session()

print("\n==============================")
print(" SCRAPER HEALTH CHECK STARTED ")
print("==============================\n")

for i, url in enumerate(URLS, start=1):
    now = time.time()
    gap = None if last_request_time is None else round(now - last_request_time, 2)

    response = session.get(url)

    status = response.status_code
    size = len(response.text)
    headers = response.request.headers
    header_count = len(headers)
    cookies_present = bool(session.cookies)

    print(f"Request #{i}")
    print(f"URL: {url}")
    print(f"Status Code: {status}")
    print(f"Response Size: {size}")
    print("Gap from last request:", "FIRST REQUEST" if gap is None else f"{gap} seconds")
    print(f"Header Count: {header_count}")
    print(f"User-Agent: {headers.get('User-Agent')}")
    print(f"Cookies Present: {cookies_present}")

    # =========================
    # DIAGNOSIS LOGIC
    # =========================
    diagnosis = []

    # 1️⃣ Hard block
    if status in (403, 429):
        diagnosis.append("HARD BLOCK (403/429)")

    # 2️⃣ Soft block
    if status == 200 and size < 2000:
        diagnosis.append("SOFT BLOCK (200 OK but empty/small HTML)")

    # 3️⃣ Rate-based suspicion
    if gap is not None and gap < 0.5:
        diagnosis.append("RATE-BASED RISK (requests too close together)")

    # 4️⃣ Header fingerprint suspicion
    if header_count <= 4:
        diagnosis.append("HEADER FINGERPRINT RISK (too few / too static headers)")

    # 5️⃣ Session / cookie issue
    if not cookies_present:
        diagnosis.append("SESSION ISSUE (no cookies, stateless requests)")

    # =========================
    # FINAL VERDICT
    # =========================
    if diagnosis:
        print("⚠️  DIAGNOSIS:")
        for d in diagnosis:
            print(f"   - {d}")
    else:
        print("✅ No obvious blocking signals detected")

    print("-" * 45)

    last_request_time = now

print("\n==============================")
print(" SCRAPER HEALTH CHECK FINISHED")
print("==============================\n")
