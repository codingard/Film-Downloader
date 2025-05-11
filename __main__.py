import os
import shutil
import asyncio
import aiohttp
from tqdm.asyncio import tqdm as tqdm_asyncio
from urllib.parse import urljoin

from logger import logger
from config import BASE_TEMP_DIR, OUTPUT_DIR, SEGMENT_LIST_FILE, MAX_CONCURRENT_DOWNLOADS
from utils.helpers import extract_slug_from_url
from utils.chrome import extract_m3u8_links
from utils.m3u8 import fetch_m3u8
from utils.download import download_segment
from utils.merge import merge_segments

async def download_video(m3u8_url, output_file):
    if os.path.exists(BASE_TEMP_DIR):
        shutil.rmtree(BASE_TEMP_DIR)
    os.makedirs(BASE_TEMP_DIR)

    logger.info("📥 Fetching M3U8 playlist...")
    m3u8_data = await fetch_m3u8(m3u8_url)
    lines = m3u8_data.splitlines()
    segments = [line for line in lines if line.endswith('.ts')]
    base_url = m3u8_url.rsplit('/', 1)[0] + '/'

    logger.info(f"🎯 Total segments found: {len(segments)}")
    sem = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

    async with aiohttp.ClientSession() as session:
        with tqdm_asyncio(total=len(segments), desc="📦 Downloading", unit="seg") as pbar:
            tasks = [
                download_segment(session, urljoin(base_url, segment), BASE_TEMP_DIR, i, sem, pbar)
                for i, segment in enumerate(segments, start=1)
            ]
            await asyncio.gather(*tasks)

    logger.info("🧠 Creating ffmpeg input list...")
    with open(SEGMENT_LIST_FILE, "w") as f:
        for i in range(1, len(segments) + 1):
            path = os.path.join(BASE_TEMP_DIR, f"seg-{i}.ts")
            if os.path.exists(path) and os.path.getsize(path) > 0:
                f.write(f"file '{path}'\n")
            else:
                logger.warning(f"⚠️ Segment is missing or corrupted: seg-{i}.ts")

    merge_segments(output_file)

    logger.info("🧹 Cleaning up temporary files...")
    shutil.rmtree(BASE_TEMP_DIR, ignore_errors=True)
    if os.path.exists(SEGMENT_LIST_FILE):
        os.remove(SEGMENT_LIST_FILE)

if __name__ == "__main__":
    try:
        url = input("🔗 Enter the URL of the video page: ").strip()
        if not url:
            logger.error("⛔ No URL provided. Exiting.")
            exit(1)

        m3u8_links = extract_m3u8_links(url)

        if not m3u8_links:
            logger.error("🚫 No .m3u8 links found on the page. Are you sure the audio track was selected?")
            exit(1)

        if len(m3u8_links) < 2:
            logger.warning("🚫 Second .m3u8 link not found. Falling back to the first one.")
            selected_link = m3u8_links[0]
        else:
            selected_link = m3u8_links[1]

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_name = extract_slug_from_url(url)
        output_path = os.path.join(OUTPUT_DIR, output_name)

        logger.info(f"🎯 Target stream: {selected_link}")
        logger.info(f"💾 Output file will be saved as: {output_path}")

        try:
            asyncio.run(download_video(selected_link, output_path))
        except aiohttp.ClientError as e:
            logger.error(f"⛔ Network error while fetching video segments: {e}")
        except asyncio.TimeoutError:
            logger.error("⛔ Timeout while fetching the .m3u8 playlist or segments.")
        except Exception as e:
            logger.exception(f"⛔ Unexpected error during download: {e}")

    except KeyboardInterrupt:
        logger.warning("⚠️ Interrupted by user.")
    except Exception as e:
        logger.exception(f"❌ Fatal error: {e}")
