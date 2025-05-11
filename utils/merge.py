import os
import shutil
import subprocess
from logger import logger
from config import SEGMENT_LIST_FILE

def merge_segments(output_file):
    logger.info("🎬 Merging .ts files using ffmpeg. This may take a while...")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", SEGMENT_LIST_FILE,
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental",
            output_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        logger.info(f"✅ Video successfully saved: {output_file}")
    except subprocess.CalledProcessError:
        logger.error("❌ ffmpeg failed during merge process.")
