import aiohttp
from config import HEADERS

async def fetch_m3u8(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()
            return await response.text()
