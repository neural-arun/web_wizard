# Module A — Foundations

## Topic 1: HTTP fundamentals (methods, headers, status codes)

### 0. Where this fits in the system (MANDATORY)
client/browser request → this component (network protocol representation) → target server → response payload

### 1. What is this
The underlying protocol for web communication. It consists of Methods (GET, POST, PUT, DELETE) indicating the action, Headers (metadata like User-Agent, Authorization, Content-Type), and Status Codes (e.g., 200 OK, 403 Forbidden, 502 Bad Gateway) representing the request outcome.

### 2. How to use this in real systems
In automation and extraction, reading status codes dictates retry logic. Modifying headers (like `User-Agent` or `Accept-Language`) is critical for disguising bots as real users.
```python
# Example: Injecting headers into a context to emulate a real user
from playwright.sync_api import sync_playwright

def fetch_data():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            extra_http_headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        page = context.new_page()
        response = page.goto("https://httpbin.org/headers")
        print(f"Status: {response.status}")
        browser.close()
```

### 3. Why does it exist
It provides a standardized, stateless contract for clients and servers to exchange data over the internet. Without it, distributed systems would lack a universal language for requesting resources and handling failures.

### 4. What happens if you remove it
- Complete inability to communicate with remote servers.
- Automation scripts fail silently because they cannot interpret server rejections (e.g., rate limits or bot blocks).
- Missing headers result in immediate CAPTCHAs or 403 Forbidden errors.

### 5. When to use vs when not to use
**Use when:**
- Making ANY network request to a REST API or web server.
- Intercepting network traffic to block resources (like images) or spoof responses.

**Avoid when:**
- Dealing with persistent, real-time bidirectional streams (where WebSockets are required instead).

### 6. Failure patterns & debugging signals (MANDATORY)
- **403 Forbidden / 401 Unauthorized:** Bot detected, missing auth token, or bad User-Agent.
- **429 Too Many Requests:** Rate limit hit. (Action: increase delays or rotate proxies).
- **502/503/504 Server Errors:** Upstream server failure or proxy timeout. (Action: apply exponential backoff).
- *Debugging:* Check the immediate response status code before attempting to parse the body.

### 7. Importance level (MANDATORY)
**Tier 1 (Critical):** Core to system correctness or stability

---

## Topic 2: HTML / DOM / CSS selectors

### 0. Where this fits in the system (MANDATORY)
raw HTTP payload → browser rendering engine → this component (DOM structure) → element location/interaction

### 1. What is this
HTML provides the skeletal structure of a web page. The DOM (Document Object Model) is the live, memory-resident tree of that structure. CSS Selectors are query strings used to locate specific nodes (elements) within the DOM tree.

### 2. How to use this in real systems
Used entirely to anchor automation scripts to the page layout. Systems rely on CSS selectors (or XPath) to find buttons to click or text to extract.
```python
# Example: Waiting for and extracting text using a CSS selector
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://news.ycombinator.com")
    
    # Wait for the table row to exist, then extract element
    locator = page.locator(".athing .titleline > a").first
    print("Article Title:", locator.inner_text())
    browser.close()
```

### 3. Why does it exist
It translates raw text (HTML) into an interactable API (DOM) that scripts and users can navigate. CSS selectors provide a fast, standardized way to traverse this massive tree without writing manual search algorithms.

### 4. What happens if you remove it
- "Element not found" exceptions crash the worker.
- If selectors are fragile (e.g., tied to generated class names like `div > span:nth-child(3)`), UI updates immediately break the extraction pipeline.
- StaleElementReference errors occur when the DOM updates but the script holds an old reference.

### 5. When to use vs when not to use
**Use when:**
- Interacting with static or predictably structured web pages.
- Scraping text that is baked into the UI rather than available via XHR/APIs.

**Avoid when:**
- The page uses aggressive dynamic class names (React/Tailwind obfuscation) and role-based or test-id selectors are available instead.
- The data can be intercepted cleanly via pure JSON API responses instead of DOM scraping.

### 6. Failure patterns & debugging signals (MANDATORY)
- **TimeoutError:** The requested selector never appeared in the DOM (page loaded too slowly or selector is wrong).
- **Strict mode violation:** The selector matched multiple elements, but the code expected exactly one.
- **Empty strings extracted:** The element was found in the DOM, but its content was overridden by CSS hidden properties or JavaScript late-loading.
- *Debugging:* Open DevTools Console and run `document.querySelectorAll('your-selector')` to verify matches.

### 7. Importance level (MANDATORY)
**Tier 1 (Critical):** Core to system correctness or stability

---

## Topic 3: Browser DevTools quick actions (Elements, Network, Console)

### 0. Where this fits in the system (MANDATORY)
human engineer → this component (DevTools inspector) → script configuration (selectors/endpoints) → parsing logic

### 1. What is this
The native diagnostic interface built into modern browsers. It allows engineers to inspect the live DOM (Elements), monitor HTTP and WebSocket traffic (Network), and execute arbitrary JavaScript against the page (Console).

### 2. How to use this in real systems
DevTools is not executed in production. It is the reverse-engineering tool used during the *development phase* to build the automation scripts that will run in production headless environments.
```python
# Typically used manually before writing this code:
# (After using DevTools Network tab to find the secret API endpoint)
import requests

api_url = "https://api.targetsite.com/v1/hidden-data" # Found via Network tab
data = requests.get(api_url).json() 
```

### 3. Why does it exist
Sites are too complex to guess selectors or APIs by reading source code. DevTools visualizes JavaScript-rendered DOMs and exposes hidden backend API calls that single-page applications (SPAs) use.

### 4. What happens if you remove it
- Engineers spend days guessing how a website loads its data.
- Extraction pipelines rely defensively on slow, flaky DOM scraping because engineers couldn't find the clean, undocumented JSON API the site uses behind the scenes.

### 5. When to use vs when not to use
**Use when:**
- Reverse-engineering a new target site.
- Debugging why an element isn't clickable in a Playwright script (e.g., an overlaid shadow div).
- Testing JavaScript snippets for `page.evaluate()`.

**Avoid when:**
- In production. Systems should rely on Playwright Tracing or API monitoring, not interactive DevTools.

### 6. Failure patterns & debugging signals (MANDATORY)
- **Missing requests in Network tab:** Page loads data via WebSockets or Server-Sent Events rather than normal XHR.
- **Element inspector shows DOM, but script fails:** The element is inside an `iframe` or Shadow DOM, which the Elements tab seamlessly hides.
- *Debugging:* Always check "Preserve log" in the Network tab to catch redirects before page reloads.

### 7. Importance level (MANDATORY)
**Tier 2 (Important):** Improves reliability, scale, or maintainability

---

## Topic 4: Playwright vs Selenium vs Scrapy vs Puppeteer comparison

### 0. Where this fits in the system (MANDATORY)
system constraints → architecture decision → this component (framework choice) → execution runtime

### 1. What is this
An architectural evaluation of automation tools. 
- **Playwright:** Modern, auto-waiting, multi-browser engine by Microsoft.
- **Selenium:** Legacy, standard protocol-based, supports older browsers.
- **Puppeteer:** Google's tool, deeply tied to Chromium/NodeJS.
- **Scrapy:** Fast, pure HTTP/HTML Python scraper (no JS rendering by default).

### 2. How to use this in real systems
Determines the footprint and capability of the worker node. For a heavy SPA, Playwright is deployed inside a large Docker container. For a simple static site, Scrapy is deployed on lightweight lambdas.
```python
# Example: The architectural result of choosing Playwright (Python async capabilities)
import asyncio
from playwright.async_api import async_playwright

async def main():
    # Playwright allows native async concurrency for high throughput
    async with async_playwright() as p:
         browser = await p.chromium.launch()
         # perform actions...
         await browser.close()
```

### 3. Why does it exist
Different extraction tasks require different tradeoffs between speed/cost and accuracy. A pure HTTP scraper (Scrapy) uses 1% of the RAM of a headful browser (Playwright), but cannot execute React.js code.

### 4. What happens if you remove it (Choosing blindly)
- Massive cloud bills: Using Playwright to parse 10M static HTML pages instead of Scrapy will inflate RAM usage and compute time unnecessarily.
- Data starvation: Attempting to use Scrapy on a heavily obfuscated SPA will yield empty HTML templates without the actual data.

### 5. When to use vs when not to use
**Use Playwright when:**
- Dealing with heavy JavaScript, SPAs, WebSockets, or multi-step logins.
- Needing native auto-waiting to reduce flaky interaction scripts.

**Avoid Playwright (Use Scrapy/Requests) when:**
- Scraping millions of static pages where compute cost and throughput are priority #1.

### 6. Failure patterns & debugging signals (MANDATORY)
- **High memory kills (OOM):** Launching too many Playwright contexts on a tiny VM. (Fix: Switch to pure HTTP requests or scale up RAM).
- **Blank page dumps:** Scrapy downloads an HTML file that only contains `<div id="root"></div>`. (Fix: Need a browser automation tool like Playwright).
- **Stale element errors:** Common in Selenium due to lack of auto-waits; highly rare in Playwright.

### 7. Importance level (MANDATORY)
**Tier 1 (Critical):** Core to system correctness or stability

---

### System Execution Flow (MANDATORY)

job received → strategy decision (Framework) → network initialization (HTTP/Headers) → page load (DOM parsing/DevTools reversed endpoints) → interaction/extraction → data standardization → output/cleanup
