from pathlib import Path

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    trace_path = Path(__file__).with_name("trace.zip")
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    page.goto("https://example.com")
    page.get_by_role("link", name="Learn more").click()
    page.wait_for_load_state("load")

    context.tracing.stop(path=str(trace_path))
    browser.close()

