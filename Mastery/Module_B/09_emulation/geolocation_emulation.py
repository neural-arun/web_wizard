from playwright.sync_api import sync_playwright


NEW_YORK_COORDINATES = {
    "latitude": 40.7128,
    "longitude": -74.0060,
}


with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    context = browser.new_context(geolocation=NEW_YORK_COORDINATES)
    context.grant_permissions(["geolocation"])

    page = context.new_page()
    page.goto("https://my-location.org")

    coordinates = page.evaluate(
        """() =>
        new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                (position) =>
                    resolve({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                    }),
                (error) => reject(error.message)
            );
        })"""
    )

    print(f"Latitude: {coordinates['latitude']}")
    print(f"Longitude: {coordinates['longitude']}")

    browser.close()
