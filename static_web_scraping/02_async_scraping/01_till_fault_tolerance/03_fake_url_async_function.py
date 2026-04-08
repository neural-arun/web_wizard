import asyncio
import random

async def fake_request(url):
    print(f"Request start: {url}")
    await asyncio.sleep(random.uniform(1,3))
    print(f"Request end: {url}")
    return f"HTML of {url}"

async def main():
    await asyncio.gather(
        fake_request("neural_arun.com"),
        fake_request("sarita_yadav.com"),
        fake_request("uday.com"),
    )

asyncio.run(main())
