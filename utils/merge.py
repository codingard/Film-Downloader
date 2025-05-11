import os
import subprocess
import platform
from logger import logger
from config import SEGMENT_LIST_FILE

def get_ffmpeg_path():
    base_dir = os.path.dirname(__file__)
    binary = "ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg"
    path = os.path.abspath(os.path.join(base_dir, "..", "ffmpeg", binary))

    if not os.path.exists(path):
        logger.error(f"❌ ffmpeg binary not found at expected path: {path}")
        logger.error("Please ensure you placed ffmpeg(.exe) in the 'ffmpeg/' folder.")
        raise FileNotFoundError("ffmpeg binary is missing.")

    return path

def merge_segments(output_file):
    ffmpeg_path = get_ffmpeg_path()

    logger.info("🎬 Merging .ts files using bundled ffmpeg...")
    try:
        subprocess.run([
            ffmpeg_path, "-y", "-f", "concat", "-safe", "0",
            "-i", SEGMENT_LIST_FILE,
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental",
            output_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        logger.info(f"✅ Video successfully saved: {output_file}")
    except subprocess.CalledProcessError:
        logger.error("❌ ffmpeg failed during the merge process.")
