from playwright.sync_api import sync_playwright

android_keywords = ("Pixel", "Galaxy", "Nexus")

with sync_playwright() as p:
    android_devices = [
        name for name in p.devices
        if any(keyword in name for keyword in android_keywords)
    ]
    print(android_devices)
