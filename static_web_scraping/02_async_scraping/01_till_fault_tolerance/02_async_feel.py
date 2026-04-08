import asyncio
import time

async def fetch(name,seconds):
    print(f"{name}, Start.")
    await asyncio.sleep(seconds)
    print(f"{name}, End.")

async def main():
    start = time.time()
    await asyncio.gather(
        fetch("A",2),
        fetch("B",2),
        fetch("C",2),
    )
    print(f"Total time: {time.time() - start}")

asyncio.run(main())
