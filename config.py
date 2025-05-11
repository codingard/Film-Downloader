from fake_useragent import FakeUserAgent

BASE_TEMP_DIR = "temp_segments"
OUTPUT_DIR = "output"
SEGMENT_LIST_FILE = "segments.txt"
MAX_RETRIES = 5
MAX_CONCURRENT_DOWNLOADS = 10

HEADERS = {
    'User-Agent': FakeUserAgent().random,
}
