# Module B — Playwright Core API (python)

## Topic 1: Install & setup (playwright, playwright-python)

### 0. Where this fits in the system (MANDATORY)
environment setup → dependency resolution → this component (Playwright bins + python bindings) → script compilation

### 1. What is this
The prerequisite libraries and browser binaries required to run Playwright in Python. It includes the `playwright` python package and the actual browser drivers installed via `playwright install`.

### 2. How to use this in real systems
Deployed via scripts in Dockerfiles or CI/CD pipelines.
```bash
# In an actual deployment pipeline
pip install playwright
playwright install chromium --with-deps
```

### 3. Why does it exist
Playwright needs matching, custom-compiled browser binaries to communicate natively with their internals, ensuring reliable interaction vs depending on random system-installed browsers.

### 4. What happens if you remove it
- `playwright install` skips: "Executable doesn't exist" errors.
- Missing dependencies crash browsers dynamically on Linux/Docker environments.

### 5. When to use vs when not to use
**Use when:** Building any fresh environment or container that runs Playwright.
**Avoid when:** Packaging pure Python scripts where dependencies cannot execute native binaries.

### 6. Failure patterns & debugging signals (MANDATORY)
- **Browser launch failure:** Missing system dependencies (e.g., `libasound2` on Ubuntu).
- *Debugging:* Always run `playwright install --with-deps` in headless Linux deployments.

### 7. Importance level (MANDATORY)
**Tier 1 (Critical):** Core to system correctness or stability

---

## Topic 2: sync vs async API (`playwright.sync_api`, `playwright.async_api`)

### 0. Where this fits in the system (MANDATORY)
system throughput requirement → this component (API mode) → script execution

### 1. What is this
The choice between executing commands sequentially (blocking, sync) or concurrently (non-blocking, async) via Python's `asyncio` loop.

### 2. How to use this in real systems
Production scrapers/crawlers *always* use `async` to run multiple contexts concurrently.
```python
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Allows multiplexing multiple tabs over one process
```

### 3. Why does it exist
Synchronous execution traps workers; you pay CPU time just waiting for packets to cross the network. Async frees the CPU to handle other tasks while waiting.

### 4. What happens if you remove it
- Using `sync_api` for huge crawls requires 1 thread/process per browser, crashing systems via memory/CPU exhaustion.

### 5. When to use vs when not to use
**Use async when:** Scaling beyond a single script (workers, queues, large batch jobs).
**Use sync when:** Running quick local debugging, one-off scripts, or pytest unit tests where concurrency isn't a goal.

### 6. Failure patterns & debugging signals (MANDATORY)
- **"Event loop is closed" / "Task was destroyed but it is pending":** Mismanaged `asyncio` loops closing before Playwright tasks finish.
- *Debugging:* Ensure `async with async_playwright()` is the absolute outermost wrapper of the async logic.

### 7. Importance level (MANDATORY)
**Tier 1 (Critical):** Core to system correctness or stability

---

## Topic 3: `async_playwright()` lifecycle

### 0. Where this fits in the system (MANDATORY)
process start → this component (lifecycle manager setup/teardown) → browser operations → process exit

### 1. What is this
The context manager that bootstraps the Node.js connection, initializes the Playwright driver server, and ensures clean shutdown of orphaned browser processes.

### 2. How to use this in real systems
Wrapped tightly around the execution core of worker scripts.
```python
# Worker execution loop pattern
async def worker_task(urls):
    async with async_playwright() as pw: # Lifecycle starts
        browser = await pw.chromium.launch()
        # Process urls
    # Lifecycle ends automatically, tearing down Node processes
```

### 3. Why does it exist
Playwright under the hood uses a Node.js server. If your Python script crashes, you need a guarantee the external Node/Chrome processes are killed. The context manager guarantees this.

### 4. What happens if you remove it
- "Zombie" chrome processes build up in the OS, causing progressive memory leaks until the whole server OOMs (Out Of Memory) crashes.

### 5. When to use vs when not to use
**Use when:** Running any playgright script. (Always).
**Avoid when:** Never. Do not instantiate the driver without a context manager.

### 6. Failure patterns & debugging signals (MANDATORY)
- **Zombie processes:** Caused by avoiding `with` blocks and manually calling `.start()/.stop()` but failing to catch exceptions.
- *Debugging:* Monitor `htop` or Process Explorer for orphaned `chrome` or `node` processes after scripts exit.

### 7. Importance level (MANDATORY)
**Tier 1 (Critical):** Core to system correctness or stability

---

## Topic 4: Browser types: Chromium / Firefox / WebKit

### 0. Where this fits in the system (MANDATORY)
script instructions → this component (rendering engine choice) → native OS rendering → website detection

### 1. What is this
The three core rendering engines Playwright supports. Each mimics the major browsers (Chrome/Edge, Firefox, Safari).

### 2. How to use this in real systems
Used during launch. Rotated explicitly when sites block one specific engine's signature.
```python
# Switching engines to bypass basic fingerprinting
browser = await p.firefox.launch()
```

### 3. Why does it exist
Provides cross-browser test coverage for QA, and crucial anti-bot evasion for extraction (some bots heavily target Chromium defaults but ignore WebKit).

### 4. What happens if you remove it
- Tied entirely to Chromium means your script breaks the moment Cloudflare or DataDome hard-bans vanilla headless Chromium signatures.

### 5. When to use vs when not to use
**Use Chromium when:** Speed and standard compatibility are needed (90% of use cases).
**Use Firefox/WebKit when:** WebKit/Safari-specific testing is needed, or Chromium is being fingerprinted/blocked by anti-bot.

### 6. Failure patterns & debugging signals (MANDATORY)
- **Unexplained 403s on Chromium:** Target is blocking Chrome-headless fingerprints.
- *Debugging:* Swap `p.chromium.launch()` to `p.firefox.launch()`. If the site loads, you have a fingerprinting issue.

### 7. Importance level (MANDATORY)
**Tier 3 (Situational):** Used in specific scenarios only

---

## Topic 5: BrowserContext vs Page

### 0. Where this fits in the system (MANDATORY)
Browser Instance → this component (isolated Context) → Page (tab) → DOM

### 1. What is this
A `Browser` is the heavy executable. A `BrowserContext` is a lightweight, isolated incognito profile (cookies, cache). A `Page` is a single tab inside that context.

### 2. How to use this in real systems
NEVER launch multiple browsers for scale. Launch ONE browser, and create MULTIPLE contexts to simulate different users.
```python
browser = await p.chromium.launch()
# Simulating User A
context_a = await browser.new_context(user_agent="MobileA")
page_a = await context_a.new_page()

# Simulating User B (isolated completely from A)
context_b = await browser.new_context(user_agent="DesktopB")
```

### 3. Why does it exist
Launching the actual Chrome executable is extremely CPU/RAM heavy (100MB+). Contexts share the executable but isolate storage, allowing 100 concurrent "users" in ~500MB of RAM instead of 10GB.

### 4. What happens if you remove it
- **Scaling fails:** Creating `browser.launch()` per task crashes the machine.
- **Data bleeding:** If using generic pages instead of Contexts, session cookies cross-pollinate and User A sees User B's auth state.

### 5. When to use vs when not to use
**Use contexts when:** Scraping with concurrency, running multi-tenant testing, rotating proxies per task.
**Avoid when:** You need full OS-level isolation natively (use Docker instead).

### 6. Failure patterns & debugging signals (MANDATORY)
- **Cookies leaking across tasks:** Engineer opened two `Pages` inside one `Context` instead of two `Contexts`.
- *Debugging:* Always track the lifetime of a Context to a specific worker task. Once the task is done, `await context.close()`.

### 7. Importance level (MANDATORY)
**Tier 1 (Critical):** Core to system correctness or stability

---

## Topic 6: Locators: CSS, XPath, text, role selectors

### 0. Where this fits in the system (MANDATORY)
interaction command → this component (dom querying strategy) → page element resolved

### 1. What is this
Methods to describe *where* an element lives in the DOM. Playwright recommends `role-based` locators (`get_by_role`) but supports CSS and XPATH natively.

### 2. How to use this in real systems
Role and text locators are robust against CSS changes.
```python
# Resilient Role-based locator
await page.get_by_role("button", name="Submit Order").click()

# Fragile CSS locator (Avoid if possible)
await page.locator("div.flex > span:nth-child(2)").click()
```

### 3. Why does it exist
HTML structures change constantly. Using semantic locators (roles, labels) ensures the script survives minor UI tweaks.

### 4. What happens if you remove it
Automations become impossibly brittle. If tied to `class="bg-blue-500"`, the script breaks the moment a developer changes the button to `bg-blue-600`.

### 5. When to use vs when not to use
**Use Roles/Text when:** Element is semantic (buttons, links, accessible forms).
**Use CSS/XPath when:** Scraping a messy layout where the data is buried in 10 layers of generated generic `div`s with no text identifiers.

### 6. Failure patterns & debugging signals (MANDATORY)
- **Strict mode violation (Multiple elements found):** `page.locator(".btn")` matches 5 buttons.
- *Debugging:* Be more specific (`.first()`, `.filter(has_text=...)`) or use `get_by_role`.

### 7. Importance level (MANDATORY)
**Tier 1 (Critical):** Core to system correctness or stability

---

## Topic 7: Actions: click, fill, type, hover, dblclick

### 0. Where this fits in the system (MANDATORY)
script intention → this component (mouse/keyboard API) → page interaction/event fired → state change

### 1. What is this
The standard verbs used to mutate the state of a page. Playwright automatically waits for actionability (visible, stable, enabled) before firing these.

### 2. How to use this in real systems
Always invoked on a resolved locator. Real systems often inject slight delays to mimic human input.
```python
# Filling a form safely
await page.get_by_label("Username").fill("user123")
await page.get_by_text("Login").click(delay=200) # delay simulates mouse down/up
```

### 3. Why does it exist
Scripts cannot just inject text into the DOM. They must emit native OS-level keyboard/mouse events to trigger React/Vue event listeners.

### 4. What happens if you remove it
- Bypassing standard actions and using `page.evaluate("document.querySelector('...').value = '123'")` fails because React synthetic events (like `onChange`) won't fire, and the site will submit an empty form.

### 5. When to use vs when not to use
**Use when:** Standard interacting with a page UI.
**Avoid when:** Need ultra-stealth behavior where default straight-line mouse movements of `.click()` get detected (use a stealth cursor plugin instead).

### 6. Failure patterns & debugging signals (MANDATORY)
- **TimeoutError during action:** Element is present but *covered* by another element (e.g., a sticky header or cookie banner).
- *Debugging:* Check for invisible overlays. Playwright logs "element was intercepted by...". Use `click(force=True)` if desperate.

### 7. Importance level (MANDATORY)
**Tier 1 (Critical):** Core to system correctness or stability

---

## Topic 8: Navigation & routing: `page.goto()`, `page.wait_for_load_state()`

### 0. Where this fits in the system (MANDATORY)
url assignment → this component (network negotiation & DOM readiness) → fully loaded page

### 1. What is this
The mechanism to direct the browser to a URL and wait to guarantee that the required assets (DOM, network data) have finished loading.

### 2. How to use this in real systems
Dictates the start of a flow. Avoid default wait states if optimizing for pure raw speed.
```python
# Waiting for the network to be mostly silent before proceeding
await page.goto("https://heavy-site.com", wait_until="networkidle")

# Explicit state waiting
await page.wait_for_load_state("domcontentloaded")
```

### 3. Why does it exist
Browsers load asynchronously. SPAs return an empty `<div id="root">` instantly. Without load state detection, scripts would proceed immediately and extract nothing.

### 4. What happens if you remove it
- Race conditions: Script tries to click a button before the JS to render the button has downloaded. Scripts pass 50% of the time and fail 50% of the time (flaky).

### 5. When to use vs when not to use
**Use `networkidle` when:** Scraping a nasty SPA where you don't know what specific element to wait for.
**Avoid `networkidle` when:** A page has a persistent polling socket or streaming video (it will NEVER reach networkidle and will timeout).

### 6. Failure patterns & debugging signals (MANDATORY)
- **Navigation Timeout (30000ms):** The page failed to reach the specified state in time due to an infinitely spinning tracking pixel or sluggish ad network.
- *Debugging:* Drop `wait_until` to `"commit"` or `"domcontentloaded"` and manually `wait_for_selector` on the specific required element.

### 7. Importance level (MANDATORY)
**Tier 1 (Critical):** Core to system correctness or stability

---

## Topic 9: Waits: explicit waits, `locator.wait_for()`, `page.wait_for_selector()`

### 0. Where this fits in the system (MANDATORY)
dynamic DOM mutation → this component (polling/promises) → condition matched → script continues

### 1. What is this
Mechanisms to pause execution until a specific element exists, disappears, or attains a certain state (visible/hidden).

### 2. How to use this in real systems
Used aggressively to synchronize script execution with unpredictable frontend loading spinners and async table popups.
```python
# Wait for loading mask to disappear before acting
await page.locator(".spinner").wait_for(state="hidden")

# Now safe to extract the data
table = page.locator("#data-table")
await table.wait_for(state="visible")
```

### 3. Why does it exist
Network latency is variable. Hardcoded `time.sleep(5)` is an anti-pattern: it wastes 4 seconds if the page loads in 1 sec, and fails entirely if the page loads in 6 seconds. Explicit waits poll the DOM dynamically.

### 4. What happens if you remove it
Relying on implicit actions or hard `sleeps` leads to catastrophic system unreliability and wasted compute hours.

### 5. When to use vs when not to use
**Use when:** A flow requires multi-step state changes (Wait for Login -> Wait for Dashboard Load -> Wait for Table Render).
**Avoid when:** Blindly waiting for things that might not exist without fallback error handling.

### 6. Failure patterns & debugging signals (MANDATORY)
- **Stuck pipelines:** A worker waits 30s for a modal, but a site bug caused the modal to never render.
- *Debugging:* Wrap critical `wait_for()` calls in try/except blocks to log custom telemetry or trigger alternative recovery flows.

### 7. Importance level (MANDATORY)
**Tier 2 (Important):** Improves reliability, scale, or maintainability

---

## Topic 10: Tracing, screenshots, PDFs, video recording

### 0. Where this fits in the system (MANDATORY)
automation execution → this component (telemetry & media capture) → artifact storage (S3/Logs)

### 1. What is this
Playwright's native capability to record everything the browser does: exact DOM snapshots, network traffic, console logs, screenshots, and videos.

### 2. How to use this in real systems
Always enabled on failure in CI pipelines, or selectively returned by APIs acting as document-renderers.
```python
# Start trace
await context.tracing.start(screenshots=True, snapshots=True)
try:
    # flow
    pass
except Exception:
    # On fail, save state to ship to artifact store
    await context.tracing.stop(path="trace-fail.zip")
```

### 3. Why does it exist
You cannot SSH into a headless browser running in a Kubernetes pod at 3am. You need physical artifacts to deduce *why* an element wasn't found (was it a Cloudflare captcha page? Or an A/B test UI?).

### 4. What happens if you remove it
- "TimeoutError on #login-btn" in logs. Engineers spend days guessing why the login failed because they can't see the screen the bot saw.

### 5. When to use vs when not to use
**Use when:** A task fails (conditional tracing), or taking screenshots for visual regression testing.
**Avoid when:** Globally enabling video/traces for millions of successful runs—it will exhaust disk space immediately.

### 6. Failure patterns & debugging signals (MANDATORY)
- **Storage bloat:** Filling worker nodes to 100% capacity with orphaned traces.
- *Debugging:* Traces are your primary debugging tool. If trace shows an empty page, check the network tab inside the trace.

### 7. Importance level (MANDATORY)
**Tier 2 (Important):** Improves reliability, scale, or maintainability

---

## Topic 11: Emulation: viewport, device, user-agent, geolocation

### 0. Where this fits in the system (MANDATORY)
script config → this component (browser fingerprint spoofer) → outgoing network requests & JS env

### 1. What is this
Mechanisms to lie to the target website about who is visiting. Tricks the site into rendering mobile layouts or granting localized content based on injected GPS coordinates.

### 2. How to use this in real systems
Crucial for bypassing basic bot detection or scraping mobile-only endpoint data (Instagram, TikTok).
```python
iphone_13 = p.devices['iPhone 13']
context = await browser.new_context(
    **iphone_13,
    geolocation={"latitude": 48.8566, "longitude": 2.3522},
    permissions=["geolocation"]
)
```

### 3. Why does it exist
Provides vast flexibility to test responsive apps cleanly. For extraction, it avoids the highly-suspicious "800x600 Headless Chrome" default fingerprint.

### 4. What happens if you remove it
- The bot screams "I am an automated script". Blocks happen instantly.
- Sites serve desktop HTML, missing key data that might be easier to parse in the simpler mobile HTML version.

### 5. When to use vs when not to use
**Use when:** Randomizing worker signatures to avoid bans, or testing specific mobile UI flows.
**Avoid when:** The target site natively checks WebGL or Canvas hashes and realizes your User-Agent claims to be a Mac but your OS renders fonts like Alpine Linux. (Advanced anti-bot requires more than just User-Agent spoofing).

### 6. Failure patterns & debugging signals (MANDATORY)
- **Layout breaks:** Forcing a small viewport hides the button the script expects to click (it becomes buried under a hamburger menu).
- *Debugging:* Take a screenshot. If dealing with mobile emulation, ensure scripts click the menu toggle first.

### 7. Importance level (MANDATORY)
**Tier 2 (Important):** Improves reliability, scale, or maintainability

---

## Topic 12: File upload & download handling

### 0. Where this fits in the system (MANDATORY)
worker file system → this component (I/O bridge) → page file input / output stream

### 1. What is this
The ability to push local files into `<input type="file">` elements, or intercept and save files originating from a browser download event.

### 2. How to use this in real systems
Hook download events concurrently with click events.
```python
# Handling downloads securely
async with page.expect_download() as download_info:
    await page.get_by_text("Export CSV").click()
download = await download_info.value
await download.save_as(f"/temp/{download.suggested_filename}")
```

### 3. Why does it exist
Downloading securely via standard HTTP requests often fails if the download requires complex cookie auth or CSRF tokens dynamically tied to the browser session. Allowing the browser to handle the download directly solves auth inheritance.

### 4. What happens if you remove it
Engineers try to regex out the download URL and pass it to Python's `requests` library, which receives a 401 Unauthorized because it lacks the browser's deeply nested session context.

### 5. When to use vs when not to use
**Use when:** Extracting invoice PDFs, reports, or pushing test images in automated QA.
**Avoid when:** The file is a publicly accessible URL (just use `httpx`/`requests` to save RAM vs loading it into Playwright).

### 6. Failure patterns & debugging signals (MANDATORY)
- **Ghost downloads:** The file stream begins saving but the Context/Page closes prematurely, resulting in a corrupted 0KB file.
- *Debugging:* Ensure `download.save_as()` is `await`ed completely before allowing the worker block to exit.

### 7. Importance level (MANDATORY)
**Tier 3 (Situational):** Used in specific scenarios only

---

## Topic 13: Frames & iframes, child frames

### 0. Where this fits in the system (MANDATORY)
main page → this component (isolated document islands) → scoped locators

### 1. What is this
Webpages embedded inside other webpages. Elements inside an iframe belong to an entirely different DOM tree and cannot be queried from the main page directly.

### 2. How to use this in real systems
You must explicitly pivot context into the frame locator.
```python
# Accessing a Stripe/Payment form buried in an iframe
frame = page.frame_locator("#payment-iframe")
await frame.locator("#card-number").fill("42424242")
```

### 3. Why does it exist
Modern web security prevents main pages from touching sensitive third-party integrations (payments, captchas, ads). The boundary must be explicitly crossed via APIs.

### 4. What happens if you remove it
- Engineer inspects DevTools: "The button is right there!"
- Playwright script: "TimeoutError. Element not found."
- Systems fail to solve captchas or checkout carts.

### 5. When to use vs when not to use
**Use when:** Interacting with Recaptcha, Stripe, embedded Youtube videos, or legacy enterprise software portals.

### 6. Failure patterns & debugging signals (MANDATORY)
- **Cross-origin frame errors:** Attempting to run `page.evaluate()` referencing iframe nodes.
- *Debugging:* If an element is visibly there but Playwright can't find it, it's almost always in an iframe or Shadow DOM. Check the DevTools DOM tree hierarchy.

### 7. Importance level (MANDATORY)
**Tier 2 (Important):** Improves reliability, scale, or maintainability

---

## Topic 14: Shadow DOM access

### 0. Where this fits in the system (MANDATORY)
custom element → this component (hidden encapsulation boundary) → scoped DOM

### 1. What is this
A web standard that encapsulates CSS and HTML inside custom web components (e.g., `<my-slider>`), hiding the internal nodes from global `document.querySelectorAll()`.

### 2. How to use this in real systems
Playwright penetrates open Shadow DOMs by default, unlike Selenium. You rarely need to do anything special conceptually, but you must chain locators.
```python
# Playwright traverses into shadow-root seamlessly
await page.locator("my-custom-element >> css=button").click()
```

### 3. Why does it exist
Developers use it to stop global website CSS from leaking into and breaking their complex standalone widget components.

### 4. What happens if you remove it
If tools can't access Shadow DOM organically (like legacy Selenium), workers resort to complex, undocumented JS execution hacks (`element.shadowRoot.querySelector`) to pierce the boundary, causing extreme flakiness.

### 5. When to use vs when not to use
**Use when:** A site uses modern Web Components (e.g., Salesforce Lightning UI or custom player widgets).

### 6. Failure patterns & debugging signals (MANDATORY)
- **Closed shadow DOMs:** If developers mark the shadow DOM as `closed`, natively Playwright cannot pierce it.
- *Debugging:* In DevTools, look for `#shadow-root (open)`. Playwright handles this out-of-the-box, but CSS paths must be accurately chained.

### 7. Importance level (MANDATORY)
**Tier 3 (Situational):** Used in specific scenarios only

---

## Topic 15: Handling dialogs, alerts, confirm, prompt

### 0. Where this fits in the system (MANDATORY)
page JS execution (`alert();`) → this component (dialog listener hook) → runtime resolution

### 1. What is this
JavaScript-native browser modals. By default, Playwright automatically DISMISSES all of these so they don't block the execution loop.

### 2. How to use this in real systems
Must intercept the dialogue event if you want to click "Accept" instead of the default auto-dismiss.
```python
async def handle_dialog(dialog):
    print(f"Message: {dialog.message}")
    await dialog.accept() # Or dismiss()

page.on("dialog", handle_dialog)
await page.get_by_text("Delete Account").click() # Triggers the confirm()
```

### 3. Why does it exist
Native alerts completely pause JavaScript execution on the browser thread until answered. In headless automation, if not answered, the entire worker pipeline deadlocks infinitely. Playwright's auto-dismiss prevents systemic deadlocks.

### 4. What happens if you remove it
- Total Pipeline Lockup. A simple `window.alert("Welcome")` renders the entire Playwright worker permanently paralyzed because there is no human to click "OK".

### 5. When to use vs when not to use
**Use explicit hooks when:** You expect a `confirm()` box (e.g., clicking a delete button to clear test state in QA) and specifically need to ACCEPT it.
**Avoid when:** You don't care about the alert; rely on the built-in auto-dismiss.

### 6. Failure patterns & debugging signals (MANDATORY)
- **Unintended unhooking:** Developer hooks the dialog on one page, but navigation destroys the page object and the hook is lost.
- *Debugging:* Ensure the `.on("dialog", ...)` is bound immediately upon creating the `Page` object.

### 7. Importance level (MANDATORY)
**Tier 2 (Important):** Improves reliability, scale, or maintainability

---

### System Execution Flow (MANDATORY)

job received → context lifecycle managed (`async_playwright`) → spoof constraints applied (Emulation) → isolated engine launched (Browser/Context) → routing & initialization (Navigation) → event hooks bound (Dialogs) → DOM wait barriers passed (Waits) → execution performed (Actions in Frames/Shadow DOM) → telemetry recorded (Traces/Downloads) → artifacts saved & automatic cleanup
