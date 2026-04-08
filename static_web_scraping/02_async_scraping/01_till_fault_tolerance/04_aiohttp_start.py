import asyncio
import aiohttp # library hai jo internet se data mangti hai but python ko rokti nhi hai.

async def main():
    session = aiohttp.ClientSession()
    print(session)
    await session.close()
# ye sahi tareeka nahi hai session open karne ka. always use with so you can close it later (automatically).
asyncio.run(main())