import os
import asyncio
import aiohttp
from config import MAX_RETRIES, HEADERS
from logger import logger

async def download_segment(session, segment_url, path, segment_number, sem, progress_bar):
    attempt = 0
    async with sem:
        while attempt < MAX_RETRIES:
            try:
                async with session.get(segment_url, headers=HEADERS, timeout=30) as response:
                    if response.status == 200:
                        content = await response.read()
                        with open(os.path.join(path, f"seg-{segment_number}.ts"), "wb") as f:
                            f.write(content)
                        progress_bar.update(1)
                        return
            except Exception as e:
                attempt += 1
                if attempt >= MAX_RETRIES:
                    logger.error(f"❌ Failed to download segment {segment_number}: {e}")
                await asyncio.sleep(2)
