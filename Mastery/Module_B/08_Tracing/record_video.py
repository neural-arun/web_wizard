from pathlib import Path

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    video_dir = Path(__file__).parent
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        record_video_dir=str(video_dir),
        record_video_size={"width": 1280, "height": 720},
    )

    page = context.new_page()
    page.goto("https://example.com")
    page.wait_for_load_state("load")
    page.get_by_role("link", name="Learn more").click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

    context.close()
    browser.close()
